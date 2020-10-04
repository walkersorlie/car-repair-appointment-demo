# Generated by Django 3.1.1 on 2020-10-01 18:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=70)),
                ('last_name', models.CharField(max_length=70)),
                ('phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+\\d{8,15}$')])),
                ('email_address', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_year', models.CharField(max_length=20)),
                ('vehicle_model', models.CharField(max_length=20)),
                ('appointment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_appointment.appointmentuser')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_repair', models.TextField()),
                ('appointment_time', models.DateTimeField()),
                ('appointment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repair_appointment.appointmentuser')),
            ],
        ),
    ]