from django.shortcuts import get_object_or_404, render, redirect
from patients.models import Patient, Appointment
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from doctors.models import Doctor, Specialty
from clinics.models import Clinic
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
import calendar
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    if request.method == 'POST':
        if 'patient_id' in request.POST and request.POST['patient_id'] != '':
            patient_id = request.POST['patient_id']
            patient = get_object_or_404(Patient, patient_id=patient_id)
            patient.ssn = request.POST['mssn'] if '*' not in request.POST['mssn'] else request.POST['ssn']
            
        else:
            patient = Patient()
            patient.ssn = request.POST['ssn']
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
    visits = Appointment.objects.filter(
            patient=patient, appointment_date_time__lt=timezone.now()
        ).order_by('appointment_date_time')
    appointments = Appointment.objects.filter(
            patient=patient, appointment_date_time__gt=timezone.now()
        ).order_by('appointment_date_time')
    
    specialities = Specialty.objects.all()
    doctors = Doctor.objects.all()
    return render(request,'view_patient.html',{'patient':patient,'visits':visits,'appointments':appointments,'specialities':specialities,'doctors':doctors})

@api_view(['GET'])
def clinics_for_procedure(request, procedure_id):
    try:
        specialty = Specialty.objects.get(id=procedure_id)
        clinics = Clinic.objects.filter(doctors__specialities=specialty).distinct()
        return Response([{"id": clinic.clinic_id, "name": clinic.name} for clinic in clinics])
    except Specialty.DoesNotExist:
        return Response({"error": "Specialty not found"}, status=404)

@api_view(['GET'])
def doctors_for_procedure_and_clinic(request, procedure_id, clinic_id):
    try:
        specialty = Specialty.objects.get(id=procedure_id)
        clinic = Clinic.objects.get(clinic_id=clinic_id)
        doctors = Doctor.objects.filter(specialities=specialty, clinics=clinic)
        return Response([{"id": doctor.doctor_id, "name": doctor.name} for doctor in doctors])
    except (Specialty.DoesNotExist, Clinic.DoesNotExist):
        return Response({"error": "Specialty or Clinic not found"}, status=404)

@api_view(['GET'])
def available_timeslots(request, doctor_id, clinic_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    clinic = get_object_or_404(Clinic, clinic_id=clinic_id)

    doctor_clinic = doctor.doctor_clinic_set.get(clinic=clinic)
    working_schedule = doctor_clinic.working_schedule
 
    days_part, time_part = working_schedule.split('|')
    days_list = [day.strip() for day in days_part.split(',')]
    start_time_str, end_time_str = [time.strip() for time in time_part.split('-')]

    day_mapping = {day[:3].lower(): index for index, day in enumerate(calendar.day_name)}
    days_num = [day_mapping[day.lower()[:3]] for day in days_list]
    
    start_time = datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()

    available_slots = []
    current_date = timezone.localdate()
    days_to_check = 60 

    while len(available_slots) < 10 and days_to_check > 0:
        if current_date.weekday() in days_num:
            start_datetime = timezone.make_aware(datetime.combine(current_date, start_time))
            end_datetime = timezone.make_aware(datetime.combine(current_date, end_time))
            
            current_slot = start_datetime
            while current_slot < end_datetime and len(available_slots) < 10:
                slot_end = current_slot + timedelta(minutes=30) 
                if slot_end <= timezone.now():
                    current_slot = slot_end
                    continue
                
                is_booked = Appointment.objects.filter(
                    doctor=doctor,
                    clinic=clinic,
                    appointment_date_time__range=[current_slot, slot_end]
                ).exists()
                
                if not is_booked:
                    available_slots.append(current_slot.strftime('%Y-%m-%d %I:%M %p'))
                
                current_slot = slot_end
        
        current_date += timedelta(days=1)
        days_to_check -= 1

    return JsonResponse(available_slots, safe=False)

    
def schedule_appointment(request,patient_id):
    if request.method == "POST" and request.POST['procedure']:
        appointment = Appointment()
        appointment.procedure = Specialty.objects.get(pk=request.POST['procedure'])
        appointment.doctor = Doctor.objects.get(pk=request.POST['doctor'])
        appointment.clinic = Clinic.objects.get(pk=request.POST['clinic'])
        appointment.patient = Patient.objects.get(pk=patient_id)
        appointment.date_booked = datetime.now()
        appointment_datetime_str = request.POST['appointment_datetime']
        appointment.appointment_date_time = datetime.strptime(appointment_datetime_str, '%Y-%m-%d %I:%M %p')
        appointment.is_visited = False
        appointment.save()
    return HttpResponseRedirect(reverse('view_patient', args=(patient_id,)))