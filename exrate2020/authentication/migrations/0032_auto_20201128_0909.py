# Generated by Django 3.1.1 on 2020-11-28 09:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0031_auto_20201125_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('7e124bdf-a312-414d-b13c-9498984777ef')),
        ),
    ]
