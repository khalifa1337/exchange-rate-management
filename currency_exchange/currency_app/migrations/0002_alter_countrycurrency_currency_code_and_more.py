# Generated by Django 4.2.13 on 2024-05-27 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrycurrency',
            name='currency_code',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='countrycurrency',
            name='currency_name',
            field=models.CharField(max_length=4),
        ),
    ]