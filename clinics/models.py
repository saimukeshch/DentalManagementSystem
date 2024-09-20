from django.db import models
from django.apps import apps
from django.utils.text import slugify

class Clinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    
    def __str__(self):
        return self.name

    @property
    def number_of_affiliated_doctors(self):
        return self.doctors.count()
    
    @property
    def affiliated_doctors(self):
        return self.doctors.all()
    
    @property
    def number_of_affiliated_patients(self):
        Appointment = apps.get_model('patients', 'Appointment')
        return Appointment.objects.filter(clinic=self).values('patient').distinct().count()