# Generated by Django 3.1.1 on 2020-11-25 08:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0030_auto_20201125_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('21fcb58c-a71d-4abf-88c1-678ceac26424')),
        ),
    ]
