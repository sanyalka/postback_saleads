# Generated manually for initial Saleads postback models.
import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Код в ссылке')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Секретный токен')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
            ],
            options={'verbose_name': 'Кампания', 'verbose_name_plural': 'Кампании', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='PostbackEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('click', 'Клик'), ('processing', 'Конверсия в обработке'), ('approved', 'Конверсия подтверждена'), ('rejected', 'Конверсия отклонена')], max_length=20, verbose_name='Статус')),
                ('click_id', models.CharField(blank=True, max_length=255, verbose_name='clickId')),
                ('conversion_id', models.CharField(blank=True, max_length=255, verbose_name='conversionId')),
                ('offer_id', models.CharField(blank=True, max_length=255, verbose_name='offerId')),
                ('goal_id', models.CharField(blank=True, max_length=255, verbose_name='goalId')),
                ('profit', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='profit')),
                ('order_sum', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='sum')),
                ('custom', models.CharField(blank=True, max_length=1024, verbose_name='custom')),
                ('raw_payload', models.JSONField(blank=True, default=dict, verbose_name='Все параметры')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP адрес')),
                ('user_agent', models.TextField(blank=True, verbose_name='User-Agent')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Получено')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='postbacks.campaign', verbose_name='Кампания')),
            ],
            options={'verbose_name': 'Постбек', 'verbose_name_plural': 'Постбеки', 'ordering': ['-created_at']},
        ),
        migrations.AddIndex(model_name='postbackevent', index=models.Index(fields=['campaign', 'status'], name='postbacks_p_campaig_c7c8ef_idx')),
        migrations.AddIndex(model_name='postbackevent', index=models.Index(fields=['conversion_id'], name='postbacks_p_convers_5a8605_idx')),
        migrations.AddIndex(model_name='postbackevent', index=models.Index(fields=['click_id'], name='postbacks_p_click_i_301ae9_idx')),
        migrations.AddIndex(model_name='postbackevent', index=models.Index(fields=['created_at'], name='postbacks_p_created_a80ebe_idx')),
    ]
