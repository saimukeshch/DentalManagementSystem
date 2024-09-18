from django.shortcuts import get_object_or_404, render
from clinics.models import Clinic
from django.db.models import Q

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
    
    doctors = clinic.affiliated_doctors
    
    print(doctors)
    
    return render(request,'view_clinic.html',{'clinic':clinic,'doctors':doctors})

def delete_clinic(request):
    return render(request,'delete_clinic.html')