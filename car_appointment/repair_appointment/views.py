import uuid
import datetime
from . import forms
from . import models
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView
from django.template.loader import render_to_string


class RequestActivationView(CreateView):
    template_name = 'repair_appointment/request_activation.html'
    form_class = forms.RequestActivationForm
    model = models.AppointmentUser
    success_url = reverse_lazy('repair_appointment:request_activation_confirmed')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.first_name = ''
        user.last_name = ''
        user.phone_number = ''
        user.email = form.cleaned_data['email_address']

        user.save()
        context = {
            'user_id': user.id,
            'protocol': self.request.scheme,
            'domain': self.request.get_host
        }
        form.send_email(context)

        return super().form_valid(form)



class RequestAppointmentView(TemplateView):
    template_name = 'repair_appointment/request_appointment.html'

    def get_context_data(self, **kwargs):
        context = super(RequestAppointmentView, self).get_context_data(**kwargs)
        user = models.AppointmentUser.objects.get(pk=self.kwargs['uid'])
        user_forms_data = {}
        if user.is_activated:
            user_forms_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number
            }
            user_form = forms.AppointmentUserForm(initial=user_forms_data, prefix='user_form')

            appointment_instance = user.appointmentrequest_set.order_by('pk')[0]
            appointment_form_data = {
                'vehicle_repair': appointment_instance.vehicle_repair,
                'appointment_time': appointment_instance.appointment_time
            }
            appointment_form = forms.RequestAppointmentForm(initial=appointment_form_data, prefix='appointment_form')

            vehicle_instance = user.vehicle_set.order_by('pk')[0]
            vehicle_form_data = {
                'vehicle_year': vehicle_instance.vehicle_year,
                'vehicle_make': vehicle_instance.vehicle_make,
                'vehicle_model': vehicle_instance.vehicle_model
            }
            vehicle_form = forms.VehicleForm(initial=vehicle_form_data, prefix='vehicle_form')

            context['is_activated'] = True
        else:
            user_form = forms.AppointmentUserForm(prefix='user_form')
            appointment_form = forms.RequestAppointmentForm(prefix='appointment_form')
            vehicle_form = forms.VehicleForm(prefix='vehicle_form')

        context['user_form'] = user_form
        context['user_forms_data'] = user_forms_data
        context['appointment_form'] = appointment_form
        context['vehicle_form'] = vehicle_form
        context['id'] = self.kwargs['uid']

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        user_form = forms.AppointmentUserForm(self.request.POST, prefix='user_form')
        appointment_form = forms.RequestAppointmentForm(self.request.POST, prefix='appointment_form')
        vehicle_form = vehicle_form = forms.VehicleForm(self.request.POST, prefix='vehicle_form')

        if user_form.is_valid() and appointment_form.is_valid() and vehicle_form.is_valid():
            user_instance = get_object_or_404(models.AppointmentUser, pk=self.kwargs['uid'])
            user_instance.first_name = user_form.cleaned_data['first_name']
            user_instance.last_name = user_form.cleaned_data['last_name']
            user_instance.phone_number = user_form.cleaned_data['phone_number']
            user_instance.is_activated = True
            user_instance.save()

            appointment_request_instance = models.AppointmentRequest(appointment_user=user_instance, vehicle_repair=appointment_form.cleaned_data['vehicle_repair'], appointment_time=appointment_form.cleaned_data['appointment_time'])
            appointment_request_instance.save()

            vehicle_instance = models.Vehicle(appointment_user=user_instance, vehicle_year=vehicle_form.cleaned_data['vehicle_year'], vehicle_model=vehicle_form.cleaned_data['vehicle_model'], vehicle_make=vehicle_form.cleaned_data['vehicle_make'])
            vehicle_instance.save()

            to_user_email_context = {
                'appointment': appointment_request_instance,
                'email': user_instance.email_address,
            }
            subject = 'Car Repair Appointment Confirmation'
            email_body = render_to_string('repair_appointment/user_request_appointment_confirmed_email.html', to_user_email_context)
            email_from = 'walkersorlie@gmail.com'
            recipient_list = [user_instance.email_address]
            send_mail(subject, email_body, email_from, recipient_list)

            internal_confirmation_email_context = {
                'user': user_instance,
                'appointment': appointment_request_instance,
                'vehicle': vehicle_instance,
                'ip_address': request.META['REMOTE_ADDR'],
            }
            email_body = render_to_string('repair_appointment/internal_appointment_request_confirm_email.html', internal_confirmation_email_context)
            recipient_list = ['repairs@example.com']
            send_mail(subject, email_body, email_from, recipient_list)

            return HttpResponseRedirect(reverse('repair_appointment:request_appointment_confirmed'))
        else:
            return self.form_invalid(request, user_form, appointment_form, vehicle_form, **kwargs)

    def form_invalid(self, request, user_form, appointment_form, vehicle_form, **kwargs):
        user_form.prefix = 'user_form'
        appointment_form.prefix = 'appointment_form'
        vehicle_form.prefix = 'vehicle_form'

        context = {
            'user_form': user_form,
            'appointment_form': appointment_form,
            'vehicle_form': vehicle_form,
        }

        return render(request, self.template_name, context)



def request_activation_confirmed_view(request):
    return render(request, 'repair_appointment/request_activation_confirmed.html')


def request_appointment_confirmed_view(request):
    return render(request, 'repair_appointment/request_appointment_confirmed.html')
