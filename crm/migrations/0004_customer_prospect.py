# Generated by Django 3.2.15 on 2022-10-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20221017_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='prospect',
            field=models.BooleanField(default=True),
        ),
    ]
