# Generated by Django 3.1.1 on 2020-10-20 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0016_auto_20201017_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shippingaddress', to=settings.AUTH_USER_MODEL),
        ),
    ]