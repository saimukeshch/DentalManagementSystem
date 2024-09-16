from django.db import models
from clinics.models import Clinic
from django.apps import apps
class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    npi = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    specialties = models.ManyToManyField('Specialty', related_name='doctors')
    clinics = models.ManyToManyField(Clinic, related_name='doctors')

    def __str__(self):
        return self.name

    @property
    def number_of_affiliated_clinics(self):
        return self.clinics.count()

    @property
    def number_of_affiliated_patients(self):
        Appointment = apps.get_model('patients', 'Appointment')
        return Appointment.objects.filter(doctor=self).values('patient').distinct().count()
    
    @property
    def specialties_names(self):
        return ', '.join(self.specialties.values_list('name', flat=True))
    
class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name