# Generated by Django 5.2.4 on 2025-07-12 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='store',
            options={},
        ),
        migrations.AddField(
            model_name='store',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='متاح لاستقبال الطلبات؟'),
        ),
    ]
