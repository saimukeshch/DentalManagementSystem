from django.db import models
from clinics.models import Clinic
from django.apps import apps
class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    npi = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    specialities = models.ManyToManyField('Specialty', related_name='doctors')
    clinics = models.ManyToManyField(Clinic, through='Doctor_Clinic', related_name='doctors')

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
    def specialities_names(self):
        return ', '.join(self.specialities.values_list('name', flat=True))
    
class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Doctor_Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    office_address = models.CharField(max_length=255)
    working_schedule = models.CharField(max_length=255)

    class Meta:
        unique_together = ('doctor', 'clinic')

    def __str__(self):
        return f"{self.doctor.name} at {self.clinic.name}"