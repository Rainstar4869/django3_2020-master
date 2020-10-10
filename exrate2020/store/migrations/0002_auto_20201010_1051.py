# Generated by Django 3.1.1 on 2020-10-10 10:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(verbose_name='creation date')),
                ('checked_out', models.BooleanField(default=False, verbose_name='checked out')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
                'ordering': ('-creation_date',),
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('d6b1de7d-fd23-426d-8cdd-9285bb7ea210'), editable=False),
        ),
    ]
