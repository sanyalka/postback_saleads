import csv
import json
from decimal import Decimal, InvalidOperation
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.db.models import Count, Sum
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from .models import Campaign, PostbackEvent

STATUS_LABELS = dict(PostbackEvent.STATUS_CHOICES)
STATUS_ORDER = [key for key, _ in PostbackEvent.STATUS_CHOICES]
STATUSES = set(STATUS_ORDER)
EXPORT_FIELDS = ['created_at', 'campaign', 'status', 'click_id', 'conversion_id', 'offer_id', 'goal_id', 'profit', 'order_sum', 'custom', 'ip_address', 'user_agent', 'raw_payload']


def _decimal(value):
    if value in (None, ''):
        return None
    try:
        return Decimal(str(value).replace(',', '.'))
    except (InvalidOperation, ValueError):
        return None


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _summary(queryset):
    counts = {status: 0 for status in STATUS_ORDER}
    for row in queryset.values('status').annotate(count=Count('id')):
        counts[row['status']] = row['count']
    return {
        'total': sum(counts.values()),
        'processing': counts[PostbackEvent.STATUS_PROCESSING],
        'approved': counts[PostbackEvent.STATUS_APPROVED],
        'rejected': counts[PostbackEvent.STATUS_REJECTED],
        'profit': queryset.aggregate(total=Sum('profit'))['total'] or 0,
    }


def _chart_rows(queryset):
    counts = {status: 0 for status in STATUS_ORDER}
    for row in queryset.values('status').annotate(count=Count('id')):
        counts[row['status']] = row['count']
    max_count = max(counts.values()) or 1
    return [
        {'status': status, 'label': STATUS_LABELS[status], 'count': counts[status], 'height': max(8, round(counts[status] / max_count * 100)) if counts[status] else 8}
        for status in STATUS_ORDER
    ]


@require_GET
def receive_postback(request, slug, status):
    if status not in STATUSES:
        raise Http404('Unknown status')
    campaign = get_object_or_404(Campaign, slug=slug, is_active=True)
    if str(campaign.token) != request.GET.get('token'):
        return JsonResponse({'ok': False, 'error': 'invalid token'}, status=403)

    event = PostbackEvent.objects.create(
        campaign=campaign,
        status=status,
        click_id=request.GET.get('clickId', ''),
        conversion_id=request.GET.get('conversionId', ''),
        offer_id=request.GET.get('offerId', ''),
        goal_id=request.GET.get('goalId', ''),
        profit=_decimal(request.GET.get('profit')),
        order_sum=_decimal(request.GET.get('sum')),
        custom=request.GET.get('custom', ''),
        raw_payload=request.GET.dict(),
        ip_address=_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )
    return JsonResponse({'ok': True, 'id': event.id, 'status': event.status})


@staff_member_required
def dashboard(request):
    campaigns = Campaign.objects.annotate(
        total=Count('events'),
        approved=Count('events', filter=models.Q(events__status=PostbackEvent.STATUS_APPROVED)),
        rejected=Count('events', filter=models.Q(events__status=PostbackEvent.STATUS_REJECTED)),
        profit_total=Sum('events__profit'),
    )
    events = PostbackEvent.objects.all()
    return render(request, 'admin/postbacks/dashboard.html', {
        'campaigns': campaigns,
        'summary': _summary(events),
        'chart_rows': _chart_rows(events),
    })


@staff_member_required
def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    events = campaign.events.all()
    links = [{'status': status, 'label': STATUS_LABELS[status], 'url': campaign.postback_url(request, status)} for status in STATUS_ORDER]
    return render(request, 'admin/postbacks/campaign_detail.html', {
        'campaign': campaign,
        'events': events[:200],
        'links': links,
        'summary': _summary(events),
        'chart_rows': _chart_rows(events),
    })


def _event_row(event):
    return {
        'created_at': event.created_at.isoformat(),
        'campaign': event.campaign.name,
        'status': event.status,
        'click_id': event.click_id,
        'conversion_id': event.conversion_id,
        'offer_id': event.offer_id,
        'goal_id': event.goal_id,
        'profit': str(event.profit) if event.profit is not None else '',
        'order_sum': str(event.order_sum) if event.order_sum is not None else '',
        'custom': event.custom,
        'ip_address': event.ip_address or '',
        'user_agent': event.user_agent,
        'raw_payload': event.raw_payload,
    }


@staff_member_required
def export_events(request, slug, fmt):
    campaign = get_object_or_404(Campaign, slug=slug)
    rows = [_event_row(event) for event in campaign.events.all()]
    if fmt == 'json':
        return JsonResponse({'campaign': campaign.name, 'events': rows}, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    if fmt == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{campaign.slug}-conversions.csv"'
        response.write('\ufeff')
        writer = csv.DictWriter(response, fieldnames=EXPORT_FIELDS)
        writer.writeheader()
        for row in rows:
            row = {**row, 'raw_payload': json.dumps(row['raw_payload'], ensure_ascii=False)}
            writer.writerow(row)
        return response
    raise Http404('Unsupported export format')
