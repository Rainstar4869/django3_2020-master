# Generated by Django 3.1.1 on 2020-11-12 11:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0026_auto_20201110_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('520edc32-d15a-4a28-8190-802523b2868e')),
        ),
    ]