# Generated by Django 4.0.4 on 2022-05-31 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service', '0004_remove_order_price_alter_orderrow_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
