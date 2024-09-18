from django.db import models
from django.apps import apps

class Clinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    @property
    def number_of_affiliated_doctors(self):
        print(self.doctors)
        return self.doctors.count()
    
    @property
    def affiliated_doctors(self):
        return self.doctors.all()
    
    @property
    def number_of_affiliated_patients(self):
        Appointment = apps.get_model('patients', 'Appointment')
        return Appointment.objects.filter(clinic=self).values('patient').distinct().count()