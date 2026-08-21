from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from .models import Campaign, PostbackEvent


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at', 'stats_link')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('token', 'created_at', 'postback_links')

    def stats_link(self, obj):
        url = reverse('postbacks:campaign_detail', kwargs={'slug': obj.slug})
        return format_html('<a href="{}">Статистика и ссылки</a>', url)
    stats_link.short_description = 'Панель'

    def postback_links(self, obj):
        if not obj.pk:
            return 'Сохраните кампанию, чтобы получить ссылки.'
        labels = dict(PostbackEvent.STATUS_CHOICES)
        items = ((labels[status], obj.postback_url(status=status)) for status, _ in PostbackEvent.STATUS_CHOICES)
        return format_html('<ul>{}</ul>', format_html_join('', '<li><strong>{}</strong>: <code>{}</code></li>', items))
    postback_links.short_description = 'Ссылки постбеков'


@admin.register(PostbackEvent)
class PostbackEventAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'campaign', 'status', 'click_id', 'conversion_id', 'profit', 'order_sum')
    list_filter = ('campaign', 'status', 'created_at')
    search_fields = ('click_id', 'conversion_id', 'offer_id', 'goal_id', 'custom')
    readonly_fields = [field.name for field in PostbackEvent._meta.fields]
    date_hierarchy = 'created_at'
