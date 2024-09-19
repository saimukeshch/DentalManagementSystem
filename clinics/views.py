from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from clinics.models import Clinic
from django.db.models import Q
from doctors.models import Doctor, Doctor_Clinic

# Create your views here.
def clinics(request):
    all_clinics = Clinic.objects.all().order_by('clinic_id')
    if request.method == 'POST':
        search_str = request.POST.get('search')
        all_clinics = all_clinics.filter(Q(name__icontains=search_str) | Q(city__icontains=search_str) | Q(state__icontains=search_str))
    for clinic in all_clinics:
        clinic.doctor = clinic.number_of_affiliated_doctors
        clinic.patient = clinic.number_of_affiliated_patients
    return render(request, 'clinics.html', {'clinics': all_clinics})

def add_clinic(request):
    return render(request,'add_clinic.html')

def edit_clinic(request):
    return render(request,'edit_clinic.html')

def view_clinic(request,clinic_id):
    clinic = get_object_or_404(Clinic, clinic_id=clinic_id)
    # affiliated_doctors = clinic.affiliated_doctors.all()
    affiliated_doctors = Doctor_Clinic.objects.filter(clinic_id=clinic_id)
    for doc in affiliated_doctors:
        doc.name = get_object_or_404(Doctor, doctor_id=doc.doctor_id)
    doctors = Doctor.objects.exclude(doctor_id__in=affiliated_doctors.values_list('doctor_id', flat=True))    
    return render(request,'view_clinic.html',{'clinic':clinic,'affiliated_doctors':affiliated_doctors,'doctors':doctors})

def delete_clinic(request):
    return render(request,'delete_clinic.html')

def add_doctor_affiliation(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_name')
        office_address = request.POST.get('office_address')
        
        # Collect working days
        working_days = request.POST.getlist('working_days')
        working_days_str = ', '.join(working_days)

        start_time = request.POST.get('working_schedule_start_time')
        end_time = request.POST.get('working_schedule_end_time')

        # Validate if a doctor is selected
        if doctor_id:
            doctor = get_object_or_404(Doctor, doctor_id=doctor_id)

            # Create a new DoctorClinic record
            doctor_clinic = Doctor_Clinic(
                doctor=doctor,
                clinic=clinic,
                office_address=office_address,
                working_schedule=f"{working_days_str} | {start_time} - {end_time}"
            )
            doctor_clinic.save()

            # Redirect to the clinic detail page (or another page)
            # return HttpResponseRedirect(reverse('clinic_detail', args=[clinic_id]))

    # If it's a GET request, render the form again
    doctors = Doctor.objects.all()  # Get all doctors for the dropdown
    return render(request, 'clinic_detail.html', {
        'clinic': clinic,
        'doctors': doctors,
    })