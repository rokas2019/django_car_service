# Generated by Django 4.0.4 on 2022-06-06 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='description',
            field=models.TextField(default='', max_length=2000, verbose_name='Aprašymas'),
        ),
    ]
