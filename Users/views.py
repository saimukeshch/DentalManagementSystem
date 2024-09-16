from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from Users.models import CustomUser

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html',{'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def user_logout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'logout.html')
    else:
        return render(request, 'dashboard.html')
    
def register(request):
    if request.method == 'POST':
        if 'user_id' in request.POST and request.POST['user_id'] != '':
            user_id = request.POST['user_id']
            
            customUser = get_object_or_404(CustomUser, user_id=user_id)
            customUser.FIRST_NAME = request.POST['first_name']
            customUser.LAST_NAME = request.POST['last_name']
            customUser.EMAIL = request.POST['email']
            customUser.PHONE = request.POST['phone']
            if 'password1' in request.POST and request.POST['password1']:
                customUser.set_password(request.POST['password1'])
            customUser.save()
            return HttpResponseRedirect(reverse('staff'))
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
        
            customUser=CustomUser.objects.create_user(
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            phone=phone if phone != '' else None)
        
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'register.html')

def dashboard(request):
    user_info = None
    if request.user.is_authenticated:
        user_info = {'email': request.user.email}
    return render(request, 'dashboard.html', {'user_info': user_info})

def clinics(request):
    all_stores = Stores.objects.all().order_by('STORE_ID')
    if request.method == 'POST':
        search_str = request.POST.get('search')
        all_stores = all_stores.filter(Q(STORE_NAME__icontains=search_str) | Q(CITY__icontains=search_str))
    return render(request, 'stores.html', {'stores': all_stores})