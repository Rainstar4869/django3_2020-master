# Generated by Django 3.1.1 on 2020-10-12 05:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20201012_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('9e2336a9-e384-405d-821f-da75d89b8bad')),
        ),
    ]