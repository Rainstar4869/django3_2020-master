# Generated by Django 3.1.1 on 2020-10-10 10:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('968ec2d5-485a-4061-aebf-c9d6bfd3962d')),
        ),
    ]
