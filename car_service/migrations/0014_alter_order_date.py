# Generated by Django 4.0.5 on 2022-06-12 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service', '0013_order_due_back'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Date'),
        ),
    ]
