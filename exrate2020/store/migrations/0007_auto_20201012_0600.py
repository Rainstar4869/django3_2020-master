# Generated by Django 3.1.1 on 2020-10-12 06:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20201012_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ecb8ffb5-104f-43f5-80c7-39ba9af955ef'), editable=False),
        ),
    ]