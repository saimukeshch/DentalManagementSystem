from django.shortcuts import render
from patients.models import Patient
from django.db.models import Q

# Create your views here.
def patients(request):
    all_patients = Patient.objects.all().order_by('patient_id')
    if request.method == 'POST':
        search_str = request.POST.get('search')
        all_patients = all_patients.filter(Q(name__icontains=search_str) | Q(address__icontains=search_str))
    return render(request, 'patients.html', {'patients': all_patients})

def add_patient(request):
    return render(request,'add_patient.html')

def edit_patient(request):
    return render(request,'edit_patient.html')

def view_patient(request):
    return render(request,'view_patient.html')

def delete_patient(request):
    return render(request,'delete_patient.html')
