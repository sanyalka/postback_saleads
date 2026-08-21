import uuid
from django.db import models
from django.urls import reverse


class Campaign(models.Model):
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('Код в ссылке', unique=True)
    token = models.UUIDField('Секретный токен', default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Кампания'
        verbose_name_plural = 'Кампании'
        ordering = ['name']

    def __str__(self):
        return self.name

    def postback_url(self, request=None, status='click'):
        path = reverse('postbacks:receive', kwargs={'slug': self.slug, 'status': status})
        url = f'{path}?token={self.token}&clickId={{clickId}}&conversionId={{conversionId}}&offerId={{offerId}}&goalId={{goalId}}&profit={{profit}}&sum={{sum}}&custom={{custom}}'
        if not request:
            return url
        return f'{request.scheme}://{request.get_host()}{url}'


class PostbackEvent(models.Model):
    STATUS_CLICK = 'click'
    STATUS_PROCESSING = 'processing'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_CLICK, 'Клик'),
        (STATUS_PROCESSING, 'Конверсия в обработке'),
        (STATUS_APPROVED, 'Конверсия подтверждена'),
        (STATUS_REJECTED, 'Конверсия отклонена'),
    ]

    campaign = models.ForeignKey(Campaign, verbose_name='Кампания', on_delete=models.CASCADE, related_name='events')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES)
    click_id = models.CharField('clickId', max_length=255, blank=True)
    conversion_id = models.CharField('conversionId', max_length=255, blank=True)
    offer_id = models.CharField('offerId', max_length=255, blank=True)
    goal_id = models.CharField('goalId', max_length=255, blank=True)
    profit = models.DecimalField('profit', max_digits=12, decimal_places=2, null=True, blank=True)
    order_sum = models.DecimalField('sum', max_digits=12, decimal_places=2, null=True, blank=True)
    custom = models.CharField('custom', max_length=1024, blank=True)
    raw_payload = models.JSONField('Все параметры', default=dict, blank=True)
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)
    user_agent = models.TextField('User-Agent', blank=True)
    created_at = models.DateTimeField('Получено', auto_now_add=True)

    class Meta:
        verbose_name = 'Постбек'
        verbose_name_plural = 'Постбеки'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['campaign', 'status']),
            models.Index(fields=['conversion_id']),
            models.Index(fields=['click_id']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.campaign} — {self.get_status_display()} — {self.created_at:%Y-%m-%d %H:%M}'
