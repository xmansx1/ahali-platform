# Generated by Django 5.2.4 on 2025-07-19 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_store_customer_delivery_share'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='delivery_policy_note',
            field=models.TextField(blank=True, help_text='مثال: الطلبات التي تقل عن 50 ريال تُحسب رسوم التوصيل 12 ريال.', verbose_name='ملاحظة سياسة التوصيل'),
        ),
    ]
