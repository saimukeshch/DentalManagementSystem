from django.shortcuts import render
from doctors.models import Doctor
from django.db.models import Q

# Create your views here.
def doctors(request):
    all_doctors = Doctor.objects.all().order_by('doctor_id')
    for doc in all_doctors:
        doc.specialities = doc.specialties_names
        doc.clinic = doc.number_of_affiliated_clinics
        doc.patient = doc.number_of_affiliated_patients
    if request.method == 'POST':
        search_str = request.POST.get('search')
        all_doctors = all_doctors.filter(Q(name__icontains=search_str))
    return render(request, 'doctors.html', {'doctors': all_doctors})

def add_doctor(request):
    return render(request,'add_doctor.html')

def view_doctor(request,doctor_id):
    return render(request,'view_doctor.html')
