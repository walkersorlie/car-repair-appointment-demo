# Generated by Django 3.1.1 on 2020-10-04 21:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair_appointment', '0004_appointmentuser_is_activated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentuser',
            name='phone_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+\\d{8,15}$')]),
        ),
    ]
