from django.shortcuts import get_object_or_404, render
from doctors.models import Doctor, Specialty
from patients.models import Patient
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.apps import apps
from django.urls import reverse

def doctors(request):
    all_doctors = Doctor.objects.all().order_by('doctor_id')
    if request.method == 'POST':
        search_str = request.POST.get('search')
        all_doctors = all_doctors.filter(Q(name__icontains=search_str)|Q(npi__icontains=search_str))

    for doc in all_doctors:
        doc.specialities_str = doc.specialities_names
        doc.clinic = doc.number_of_affiliated_clinics
        doc.patient = doc.number_of_affiliated_patients

    return render(request, 'doctors.html', {'doctors': all_doctors})

def add_doctor(request):
    if request.method == 'POST':
        if 'doctor_id' in request.POST and request.POST['doctor_id'] != '':
            doctor_id = request.POST['doctor_id']
            doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
            
        else:
            doctor = Doctor()
        doctor.npi = request.POST['npi']
        doctor.name = request.POST['name']
        doctor.email = request.POST['email']
        doctor.phone_number = request.POST['phone_number']
        doctor.save()
        
        specialities_str = request.POST.get('specialities_hidden', '')
        
        if specialities_str:
            specialities_list = [spec.strip() for spec in specialities_str.split(',')]
            
            current_specialities = doctor.specialities.all()
            
            for specialty_name in specialities_list:
                if not current_specialities.filter(name=specialty_name).exists():
                    specialty = get_object_or_404(Specialty, name=specialty_name)
                    doctor.specialities.add(specialty)
                
            for specialty in current_specialities:
                if specialty.name not in specialities_list:
                    doctor.specialities.remove(specialty)
               
        return HttpResponseRedirect(reverse('doctors'))
    return render(request, 'add_doctor.html',{'all_specialities' : Specialty.objects.all()})

def view_doctor(request,doctor_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    doctor.specialities_str = doctor.specialities_names
    Appointment = apps.get_model('patients', 'Appointment')
    patients = Appointment.objects.filter(doctor=doctor).values('patient').distinct()
    affiliated_patients =[]
    for patient in patients:
        affiliated_patients.append(get_object_or_404(Patient, patient_id = patient['patient']))
    affiliated_clinics = doctor.clinics.all()
    context = {
        'doctor': doctor,
        'affiliated_patients': affiliated_patients,
        'affiliated_clinics': affiliated_clinics,
        'all_specialities' : Specialty.objects.all()
    }
    return render(request,'view_doctor.html', context)


