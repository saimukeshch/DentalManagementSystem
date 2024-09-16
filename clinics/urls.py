from django.urls import path
from . import views

urlpatterns = [
    path('', views.clinic_list, name='clinic_list'),
]
