# Generated by Django 3.1.1 on 2020-10-05 14:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20201005_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('11ec197c-b28e-4860-aa40-6e3553fd5bc5')),
        ),
    ]