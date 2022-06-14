# Generated by Django 4.0.5 on 2022-06-09 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car_service', '0010_alter_carmodel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='car_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='car_service.carmodel'),
        ),
    ]