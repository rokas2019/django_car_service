# Generated by Django 4.0.4 on 2022-05-31 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service', '0005_order_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
