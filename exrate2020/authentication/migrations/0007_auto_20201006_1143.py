# Generated by Django 3.1.1 on 2020-10-06 11:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20201005_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('4fd739ba-af0a-48dd-aa0b-b469ec2dcba8')),
        ),
    ]
