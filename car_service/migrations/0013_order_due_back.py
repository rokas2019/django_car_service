# Generated by Django 4.0.5 on 2022-06-12 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service', '0012_car_description_orderreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='due_back',
            field=models.DateField(blank=True, null=True, verbose_name='Will be returned'),
        ),
    ]
