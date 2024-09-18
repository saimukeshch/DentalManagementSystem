from django.shortcuts import render
from patients.models import Patient, Visit, Appointment
from django.db.models import Q
from django.utils import timezone

def patients(request):
    all_patients = Patient.objects.all().order_by('patient_id')

    for patient in all_patients:
        # Get the last visit
        last_visit = Appointment.objects.filter(
            patient=patient, appointment_date_time__lt=timezone.now()
        ).order_by('appointment_date_time').first()
        
        patient.last_visit_date = last_visit.appointment_date_time if last_visit else None
        patient.last_visit_doctor = last_visit.doctor.name if last_visit else None
        patient.last_visit_procedures = last_visit.procedure.name if last_visit else None

        # Get the next appointment (using timezone.now() for current datetime)
        next_appointment = Appointment.objects.filter(
            patient=patient, appointment_date_time__gt=timezone.now()
        ).order_by('appointment_date_time').first()

        patient.next_appointment_date = next_appointment.appointment_date_time if next_appointment else None
        patient.next_appointment_doctor = next_appointment.doctor.name if next_appointment else None
        patient.next_appointment_procedure = next_appointment.procedure.name if next_appointment and next_appointment.procedure else None

    if request.method == 'POST':
        search_str = request.POST.get('search')
        all_patients = all_patients.filter(Q(name__icontains=search_str) | Q(address__icontains=search_str))
    
    return render(request, 'patients.html', {'patients': all_patients})


def add_patient(request):
    return render(request,'add_patient.html')

def edit_patient(request):
    return render(request,'edit_patient.html')

def view_patient(request,patient_id):
    return render(request,'view_patient.html')

def delete_patient(request):
    return render(request,'delete_patient.html')
