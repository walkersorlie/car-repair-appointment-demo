from django import forms
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils import timezone
from django.template.loader import render_to_string
from bootstrap_datepicker_plus import DateTimePickerInput
from . import models


class RequestActivationForm(forms.ModelForm):
    class Meta:
        model = models.AppointmentUser
        fields = ('email_address',)

    error_css_class = 'error'
    required_css_class = 'required'

    def send_email(self, context):
        user = context['user_id']
        subject = 'Car Repair Appointment Activation Email'
        email_body = render_to_string('repair_appointment/activation_email.html', context)
        email_from = 'walkersorlie@gmail.com'
        recipient_list = [self.cleaned_data['email_address']]
        send_mail(subject, email_body, email_from, recipient_list)


class AppointmentUserForm(forms.ModelForm):
    class Meta:
        model = models.AppointmentUser
        fields = ('first_name', 'last_name', 'phone_number')


class RequestAppointmentForm(forms.ModelForm):
    class Meta:
        model = models.AppointmentRequest
        fields = ('vehicle_repair', 'appointment_time')
        widgets = {
            'appointment_time': DateTimePickerInput(),
        }


    error_css_class = 'error'
    required_css_class = 'required'

    def clean_appointment_time(self):
        local_dt = self.cleaned_data['appointment_time']
        if local_dt <= timezone.now():
            raise forms.ValidationError("Please select an appointment in the future")
        return local_dt



class VehicleForm(forms.ModelForm):
    class Meta:
        model = models.Vehicle
        fields = ('vehicle_year', 'vehicle_make', 'vehicle_model')

    error_css_class = 'error'
    required_css_class = 'required'
