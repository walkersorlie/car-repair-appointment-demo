from django.test import TestCase
from django.urls import reverse, resolve
from django.core import mail
from django.template.loader import render_to_string
from . import forms, models
from uuid import UUID


class RequestActivationFormTests(TestCase):
    def test_blank_create_post_form(self):
        form = forms.RequestActivationForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form = forms.RequestActivationForm({})
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email_address': ['This field is required.'],
        })

    def test_form_valid(self):
        form = forms.RequestActivationForm()
        self.assertFalse(form.is_bound)

        form_data = {'email_address': 'valid@email.com'}
        form = forms.RequestActivationForm(data=form_data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_form_not_valid(self):
        form = forms.RequestActivationForm()
        self.assertFalse(form.is_bound)

        form_data = {'email_address': 'not valid@email.com'}
        form = forms.RequestActivationForm(data=form_data)
        self.assertTrue(form.is_bound)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email_address': ['Enter a valid email address.'],
        })

    def test_user_created_on_form_valid_post(self):
        form_data = {'email_address': 'valid@email.com'}
        form = forms.RequestActivationForm(form_data)
        response = self.client.post('/', form_data)
        self.assertTrue(isinstance(response.context['user_id'], UUID))
        self.assertEqual(models.AppointmentUser.objects.count(), 1)

    def test_send_email_on_form_valid(self):
        form_data = {'email_address': 'valid@email.com'}
        form = forms.RequestActivationForm(form_data)
        response = self.client.post(reverse('repair_appointment:request_activation'), form_data)

        user = models.AppointmentUser.objects.get(pk=response.context['user_id'])

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Car Repair Appointment Activation Email')
        self.assertEqual(mail.outbox[0].to, [user.email_address])

    def test_redirect_to_request_activation_confirmed(self):
        form_data = {'email_address': 'valid@email.com'}
        response = self.client.post(reverse('repair_appointment:request_activation'), form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('repair_appointment:request_activation_confirmed'))


class AppointmentUserFormTests(TestCase):
    def test_blank_post_request_appointment_user_form(self):
        form = forms.AppointmentUserForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form = forms.AppointmentUserForm({})
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())


class RequestAppointmentFormTests(TestCase):
    def test_blank_post_request_appointment_user_form(self):
        form = forms.RequestAppointmentForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form = forms.RequestAppointmentForm({})
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())


class VehicleFormTests(TestCase):
    def test_blank_post_request_appointment_user_form(self):
        form = forms.VehicleForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form = forms.VehicleForm({})
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
