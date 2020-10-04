# Generated by Django 3.1.1 on 2020-10-03 21:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_appointment', '0002_auto_20201002_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_make',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='appointmentuser',
            name='phone_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Minimum length 8 and up to 15 digits allowed.", regex='^\\+\\d{8,15}$')]),
        ),
    ]
