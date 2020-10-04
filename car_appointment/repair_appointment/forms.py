from django import forms
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.template.loader import render_to_string
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
        # fields = ('vehicle_repair', 'appointment_time')
        fields = ('vehicle_repair',)
        # widgets = {
        #     'appointment_time': forms.SplitDateTimeWidget(date_attrs={'class':'form-control', "type": "date"}, time_attrs={'class':'form-control', "type": "time"}),
        # }

    # appointment_time = forms.SplitDateTimeField()

    error_css_class = 'error'
    required_css_class = 'required'


class VehicleForm(forms.ModelForm):
    class Meta:
        model = models.Vehicle
        fields = ('vehicle_year', 'vehicle_make', 'vehicle_model')
