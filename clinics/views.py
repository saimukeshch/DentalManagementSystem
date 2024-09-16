from django.shortcuts import render
from clinics.models import Clinic
from django.db.models import Q

# Create your views here.
def clinics(request):
    all_clinics = Clinic.objects.all().order_by('clinic_id')
    for clinic in all_clinics:
        clinic.doctor = clinic.number_of_affiliated_doctors;
        clinic.patient = clinic.number_of_affiliated_patients;
    if request.method == 'POST':
        search_str = request.POST.get('search')
        all_clinics = all_clinics.filter(Q(name__icontains=search_str) | Q(city__icontains=search_str))
    return render(request, 'clinics.html', {'clinics': all_clinics})

def add_clinic(request):
    return render(request,'add_clinic.html')

def edit_clinic(request):
    return render(request,'edit_clinic.html')

def view_clinic(request):
    return render(request,'view_clinic.html')

def delete_clinic(request):
    return render(request,'delete_clinic.html')