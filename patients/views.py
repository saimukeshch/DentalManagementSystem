from django.shortcuts import get_object_or_404, render
from patients.models import Patient, Appointment
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

def patients(request):
    all_patients = Patient.objects.all().order_by('patient_id')

    for patient in all_patients:
        last_visit = Appointment.objects.filter(
            patient=patient, appointment_date_time__lt=timezone.now(),is_visited=True
        ).order_by('appointment_date_time').first()
        
        patient.last_visit_date = last_visit.appointment_date_time if last_visit else None
        patient.last_visit_doctor = last_visit.doctor.name if last_visit else None
        patient.last_visit_procedures = last_visit.procedure.name if last_visit else None

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
    print("called")
    if request.method == 'POST':
        print("here")
        if 'patient_id' in request.POST and request.POST['patient_id'] != '':
            patient_id = request.POST['patient_id']
            patient = get_object_or_404(Patient, patient_id=patient_id)
            patient.ssn = request.POST['mssn'] if '*' not in request.POST['mssn'] else request.POST['ssn']
            
        else:
            
            patient = Patient()
            patient.ssn = request.POST['ssn']
            print("here1")
        patient.name = request.POST['name']
        patient.address = request.POST['address']
        patient.phone_number = request.POST['phone_number']
        patient.date_of_birth = request.POST['date_of_birth']
        patient.gender = request.POST['gender']
        patient.save()
        return HttpResponseRedirect(reverse('patients'))
    return render(request,'add_patient.html')

def view_patient(request,patient_id):
    patient = Patient.objects.get(patient_id = patient_id)
    print(patient.date_of_birth)
    visits = Appointment.objects.filter(
            patient=patient, appointment_date_time__lt=timezone.now()
        ).order_by('appointment_date_time')
    appointments = Appointment.objects.filter(
            patient=patient, appointment_date_time__gt=timezone.now()
        ).order_by('appointment_date_time')
    return render(request,'view_patient.html',{'patient':patient,'visits':visits,'appointments':appointments})