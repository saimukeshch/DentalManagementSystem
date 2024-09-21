
from django.urls import path
from . import views

urlpatterns = [
    path('clinics-for-procedure/<int:procedure_id>/', views.clinics_for_procedure, name='clinics_for_procedure'),
    path('doctors-for-procedure-and-clinic/<int:procedure_id>/<int:clinic_id>/', views.doctors_for_procedure_and_clinic, name='doctors_for_procedure_and_clinic'),
    path('available-timeslots/<int:doctor_id>/<int:clinic_id>/', views.available_timeslots, name='available_timeslots'),
]