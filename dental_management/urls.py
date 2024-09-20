"""
URL configuration for dental_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Users import views
from doctors import views as docViews
from patients import views as patViews
from clinics import views as cliViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('doctors/',docViews.doctors, name = 'doctors'),
    path('clinics/',cliViews.clinics, name = 'clinics'),
    path('patients/',patViews.patients, name = 'patients'),
    path('add_clinic/',cliViews.add_clinic, name = 'add_clinic'),
    path('edit_clinic/',cliViews.edit_clinic, name = 'edit_clinic'),
    path('view_clinic/<int:clinic_id>',cliViews.view_clinic, name = 'view_clinic'),
    path('add_doctor_affiliation/<int:clinic_id>',cliViews.add_doctor_affiliation, name = 'add_doctor_affiliation'),
    path('delete_affiliation/<int:clinic_id>/<int:id>',cliViews.delete_affiliation, name = 'delete_affiliation'),
    path('add_doctor/',docViews.add_doctor, name = 'add_doctor'),
    path('view_doctor/<int:doctor_id>',docViews.view_doctor, name = 'view_doctor'),
    path('add_patient/',patViews.add_patient, name = 'add_patient'),
    path('view_patient/<int:patient_id>',patViews.view_patient, name = 'view_patient'),
]
