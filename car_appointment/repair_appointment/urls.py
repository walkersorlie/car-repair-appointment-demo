from django.urls import path
from . import views

app_name = 'repair_appointment'
urlpatterns = [
    # /
    path('', views.RequestActivationView.as_view(), name='request_activation'),

    # /activation-requested/
    path('activation-requested/', views.request_activation_confirmed_view, name='request_activation_confirmed'),

    # /appointment-requested/
    path('appointment-requested/<uuid:uid>/', views.RequestAppointmentView.as_view(), name='request_appointment'),

    #/appointment-confirmed/
    path('appointment-confirmed/', views.request_appointment_confirmed_view, name='request_appointment_confirmed'),
]
