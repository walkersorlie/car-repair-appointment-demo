import uuid
from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime, timezone
import pytz


class AppointmentUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Minimum length 8 and up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16)
    email_address = models.EmailField()
    is_activated = models.BooleanField(default=False)


class AppointmentRequest(models.Model):
    appointment_user = models.ForeignKey(AppointmentUser, on_delete=models.CASCADE)
    vehicle_repair = models.TextField()
    appointment_time = models.DateTimeField()

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         local_timestamp = datetime.timestamp(self.appointment_time)
    #         utc_dt = datetime.fromtimestamp(local_timestamp, pytz.utc)
    #         self.appointment_time = utc_dt
    #         # self.appointment_time = self.appointment_time.astimezone().astimezone(pytz.utc).replace(tzinfo=None)
    #
    #     super(AppointmentRequest, self).save(*args, **kwargs)


class Vehicle(models.Model):
    appointment_user = models.ForeignKey(AppointmentUser, on_delete=models.CASCADE)
    vehicle_year = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=20)
    vehicle_make = models.CharField(max_length=20, default='')
