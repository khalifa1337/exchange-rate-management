# Generated by Django 4.2.13 on 2024-05-29 19:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('currency_app', '0003_syncparameter_relativechange'),
    ]

    operations = [
        migrations.AddField(
            model_name='relativechange',
            name='relative_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
