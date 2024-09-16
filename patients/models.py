from django.db import models
from doctors.models import Doctor, Specialty
from clinics.models import Clinic

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    last_4_ssn = models.CharField(max_length=4)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    doctors = models.ManyToManyField(Doctor, through='Visit', related_name='patients')
    clinics = models.ManyToManyField(Clinic, through='Visit', related_name='patients')

    def __str__(self):
        return self.name


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    visit_date_time = models.DateTimeField()
    procedures_done = models.TextField()
    doctor_notes = models.TextField()

    def __str__(self):
        return f"Visit on {self.visit_date_time} by {self.patient.name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    appointment_date_time = models.DateTimeField()
    date_booked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment on {self.appointment_date_time} for {self.patient.name}"
