from django.db.models import F
from django.test import RequestFactory, TestCase
from django.urls import reverse, resolve
from django.core import mail
from django.template.loader import render_to_string
from . import forms, models, views
import uuid
import datetime
from django.utils import timezone



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
        self.assertTrue(isinstance(response.context['user_id'], uuid.UUID))
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
    def test_blank_post_appointment_user_form(self):
        form = forms.AppointmentUserForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form = forms.AppointmentUserForm({})
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_appointment_user_form_valid(self):
        form = forms.AppointmentUserForm()
        self.assertFalse(form.is_bound)

        form_data = {
            'first_name': 'first name',
            'last_name': 'last name',
            'phone_number': '+454656556565',
        }
        form = forms.AppointmentUserForm(data=form_data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_appointment_user_form_first_name_required(self):
        form = forms.RequestActivationForm()
        self.assertFalse(form.is_bound)

        form_data = {
            'first_name': '',
            'last_name': 'last name',
            'phone_number': '+454656556565',
        }
        form = forms.AppointmentUserForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'first_name': ['This field is required.'],
        })

    def test_appointment_user_form_last_name_required(self):
        form = forms.RequestActivationForm()
        self.assertFalse(form.is_bound)

        form_data = {
            'first_name': 'first name',
            'last_name': '',
            'phone_number': '+454656556565',
        }
        form = forms.AppointmentUserForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'last_name': ['This field is required.'],
        })

    def test_appointment_user_form_phone_required(self):
        form = forms.RequestActivationForm()
        self.assertFalse(form.is_bound)

        form_data = {
            'first_name': 'first name',
            'last_name': 'last name',
            'phone_number': '',
        }
        form = forms.AppointmentUserForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'phone_number': ['This field is required.'],
        })

    def test_appointment_user_form_phone_number_country_code_validation(self):
        form = forms.RequestActivationForm()
        self.assertFalse(form.is_bound)

        form_data = {
            'first_name': 'first name',
            'last_name': 'last name',
            'phone_number': '34435453535',
        }
        form = forms.AppointmentUserForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'phone_number': ["Phone number must be entered in the format: '+999999999'. Minimum length 8 and up to 15 digits allowed."],
        })

    def test_appointment_user_form_phone_number_minimum_length_validation(self):
        form = forms.RequestActivationForm()
        self.assertFalse(form.is_bound)

        form_data = {
            'first_name': 'first name',
            'last_name': 'last name',
            'phone_number': '34435',
        }
        form = forms.AppointmentUserForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'phone_number': ["Phone number must be entered in the format: '+999999999'. Minimum length 8 and up to 15 digits allowed."],
        })

    def test_appointment_user_form_phone_number_maximum_length_validation(self):
        form = forms.RequestActivationForm()
        self.assertFalse(form.is_bound)

        form_data = {
            'first_name': 'first name',
            'last_name': 'last name',
            'phone_number': '+5555555555555555344305453535',
        }
        form = forms.AppointmentUserForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'phone_number': ['Ensure this value has at most 16 characters (it has 29).'],
        })


class RequestAppointmentFormTests(TestCase):
    def test_blank_request_appointment_form(self):
        form = forms.RequestAppointmentForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form = forms.RequestAppointmentForm({})
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_valid_appointment_form(self):
        form = forms.RequestAppointmentForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form_data = {
            'vehicle_repair': 'Fix dis!',
            'appointment_time': timezone.now() + datetime.timedelta(days=1),
        }
        form = forms.RequestAppointmentForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_appointment_form_vehicle_repair_required(self):
        form = forms.RequestAppointmentForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form_data = {
            'vehicle_repair': '',
            'appointment_time': timezone.now() + datetime.timedelta(days=1),
        }
        form = forms.RequestAppointmentForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'vehicle_repair': ['This field is required.'],
        })

    def test_appointment_form_appointment_time_required(self):
        form = forms.RequestAppointmentForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form_data = {
            'vehicle_repair': 'Fix dis!',
            'appointment_time': '',
        }
        form = forms.RequestAppointmentForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'appointment_time': ['This field is required.'],
        })

    def test_appointment_form_appointment_time_reject_past_time(self):
        form = forms.RequestAppointmentForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form_data = {
            'vehicle_repair': 'Fix dis',
            'appointment_time': timezone.now(),
        }
        form = forms.RequestAppointmentForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'appointment_time': ['Please select an appointment in the future'],
        })

class VehicleFormTests(TestCase):
    def test_blank_vehicle_form(self):
        form = forms.VehicleForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form = forms.VehicleForm({})
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_valid_vehicle_form(self):
        form = forms.VehicleForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form_data = {
            'vehicle_year': '2004',
            'vehicle_make': 'Toyota',
            'vehicle_model': 'Highlander',
        }
        form = forms.VehicleForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_vehicle_form_vehicle_year_required(self):
        form = forms.VehicleForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form_data = {
            'vehicle_year': '',
            'vehicle_make': 'Toyota',
            'vehicle_model': 'Highlander',
        }
        form = forms.VehicleForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'vehicle_year': ['This field is required.'],
        })

    def test_vehicle_form_vehicle_make_required(self):
        form = forms.VehicleForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form_data = {
            'vehicle_year': '2004',
            'vehicle_make': '',
            'vehicle_model': 'Highlander',
        }
        form = forms.VehicleForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'vehicle_make': ['This field is required.'],
        })

    def test_vehicle_form_vehicle_model_required(self):
        form = forms.VehicleForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

        form_data = {
            'vehicle_year': '2004',
            'vehicle_make': 'Toyota',
            'vehicle_model': '',
        }
        form = forms.VehicleForm(form_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'vehicle_model': ['This field is required.'],
        })


class RequestAppointmentViewTests(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     cls.user = models.AppointmentUser.objects.create(first_name='Walker', last_name='Sorlie', phone_number='+34687191722', email_address='walkersorlie@walkersorlie.com', is_activated=False)

    def setUp(self):
        self.user = models.AppointmentUser.objects.create(first_name='Walker', last_name='Sorlie', phone_number='+34687191722', email_address='walkersorlie@walkersorlie.com', is_activated=False)

    def test_get_first_page_visit(self):
        response = self.client.get(reverse('repair_appointment:request_appointment', kwargs={'uid':self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.is_activated, False)

        user_form = response.context['user_form']
        self.assertTrue(user_form.fields['first_name'].label == 'First name')

        appointment_form = response.context['appointment_form']
        self.assertTrue(appointment_form.fields['vehicle_repair'].label == 'Vehicle repair')

        vehicle_form = response.context['vehicle_form']
        self.assertTrue(vehicle_form.fields['vehicle_year'].label == 'Vehicle year')

        id = response.context['id']
        self.assertEqual(self.user.pk, id)

    def test_get_page_submited_before(self):
        self.user.is_activated = True
        self.user.save()
        appointment_request = models.AppointmentRequest.objects.create(appointment_user=self.user, vehicle_repair='Fix this', appointment_time=datetime.datetime.now())
        vehicle = models.Vehicle.objects.create(appointment_user=self.user, vehicle_year='2004', vehicle_model='Highlander', vehicle_make='Toyota')

        response = self.client.get(reverse('repair_appointment:request_appointment', kwargs={'uid':self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.is_activated, True)

        self.assertContains(response, "It looks like you've already requested an appointment")
        self.assertContains(response, '+34687191722')
        self.assertContains(response, 'Highlander')
        self.assertContains(response, 'Fix this')

    # def test_post_form_invalid(self):
    #     user_forms_data = {
    #         'first_name': self.user.first_name,
    #         'last_name': self.user.last_name,
    #         'phone_number': self.user.phone_number
    #     }
    #     user_form = forms.AppointmentUserForm(user_forms_data, prefix='user_form')
    #
    #     appointment_request = models.AppointmentRequest.objects.create(appointment_user=self.user, vehicle_repair='Fix this', appointment_time=datetime.datetime.now())
    #     appointment_request_form = forms.RequestAppointmentForm(appointment_request, prefix='appointment_form')
    #
    #     vehicle = models.Vehicle.objects.create(appointment_user=self.user, vehicle_year='2004', vehicle_model='Highlander', vehicle_make='Toyota')
    #     vehicle_form = forms.VehicleForm(vehicle, prefix='vehicle_form')
    #
    #     appointment_form_data = {
    #         'vehicle_repair': '',
    #         'appointment_time': timezone.now() + datetime.timedelta(days=1),
    #     }
    #
    #     vehicle_form_data = {
    #         'vehicle_year': '2003',
    #         'vehicle_make': 'Toyota',
    #         'vehicle_model': 'Camry',
    #     }
    #
    #     post_data = {
    #         'user_form': forms.AppointmentUserForm(user_forms_data),
    #         'appointment_request_form': forms.RequestAppointmentForm(appointment_form_data),
    #         'vehicle_form': forms.VehicleForm(vehicle_form_data),
    #     }
    #
    #     response = self.client.post(reverse('repair_appointment:request_appointment', kwargs={'uid':self.user.id}), post_data)
        # print(response.content)
        # self.assertFormError(response, response.context['appointment_form'], 'vehicle_repair', ['This field is required.'])
        # for obj in response.context:
        #     print(obj)
        # print(response.status_code)
        # print(response.context['appointment_form'].data['appointment_request_form'])
        # self.assertNotContains(response.context['appointment_form'].data['appointment_request_form'], 'vehicle_repair', status_code='200')
        # test = response.context['appointment_form'].data['appointment_request_form']
        # self.assertContains(response.context['appointment_form'].data, 'vehicle_repair')
        # self.assertEqual(len(mail.outbox), 1)
        # self.assertEqual(mail.outbox[0].subject, 'Car Repair Appointment Activation Email')
        # self.assertEqual(mail.outbox[0].to, [user.email_address])
