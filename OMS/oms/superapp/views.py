from typing import Union
from datetime import timedelta
from django.db.models import Q
from django.urls import reverse
from app.models import CustomUser
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from superapp.forms import EditUsersForm
from app.forms import EditUsersDetailsForm
from app.forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from students.models import DataTableStudents, TimeLog
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

DASHBOARD = 'superapp/dashboard.html'
MAIN_DASHBOARD = 'superapp/main-dashboard.html'
HOME_URL_PATH = 'superapp/base.html'

def superHome(request) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse]:        
    return render(request, HOME_URL_PATH)

def superAdminDashboard(request) -> HttpResponse:
    return render(request, DASHBOARD)

def mainDashboard(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    # Approve
    approve = DataTableStudents.objects.filter(status='approved')
    approve_count = approve.count()
    # Pending
    pending = DataTableStudents.objects.filter(status='pending')
    pending_count = pending.count()
    # Rejected
    reject = DataTableStudents.objects.filter(status='rejected')
    reject_count = reject.count()

    return render(
        request,
        MAIN_DASHBOARD,
        {
            'approve_count': approve_count,
            'pending_count': pending_count,
            'reject_count': reject_count,
            'firstName': firstName,
            'lastName': lastName
        }
    )

def getAllTheUserAccount(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)    
    firstName = admin.first_name
    lastName = admin.last_name
    admin_users = CustomUser.objects.filter(Q(is_staff=True) or Q(is_superuser=True))
    return render(request, 'superapp/users.html', {
        'getAllTheUserAccount': admin_users,
        'firstName': firstName,
        'lastName': lastName
    })

def getActivityLogs(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    # 
    firstName = admin.first_name
    lastName = admin.last_name
    # 
    admin_users = CustomUser.objects.filter(Q(is_staff=True) or Q(is_superuser=True) or Q(is_superuser=False))
    return render(request, 'superapp/activitylogs.html', {
        'getActivityLogs': admin_users,
        'firstName': firstName,
        'lastName': lastName
    })

def editUsers(request, id): 
    toEditDetails = admin = get_object_or_404(CustomUser, pk=id)
    # 
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    # 
    firstName = admin.first_name
    lastName = admin.last_name
    
    if request.method == 'POST':
        form = EditUsersDetailsForm(request.POST, instance=toEditDetails)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('superapp:getAllTheUserAccount')
        else:
            print(form.errors)
    else:
        form = EditUsersDetailsForm(instance=toEditDetails)
    return render(request, 'superapp/edit-users.html', {
        'form': form,
        'admin': admin,
        'toEditDetails': toEditDetails,
        'firstName': firstName,
        'lastName': lastName
    })


def editUserProfile(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    if request.method == 'POST':
        form = EditUsersForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('superapp:editUserProfile')
    else:
        form = EditUsersForm(instance=admin)
    return render(request, 'superapp/profile.html', {
        'form': form,
        'firstName': firstName,
        'lastName': lastName
    })

def addUsers(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'superapp/success.html', {'message': 'Registration successful!'})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'superapp/add-users.html', {'form': form})

def createUserAdmin(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'superapp/success.html', {'message': 'Registration successful!'})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'superapp/userCreation.html', {'form': form})

def superAdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_superuser:
                login(request, user)
                return redirect('superapp:superAdminDashboard')
            else:
                messages.error(request, 'You do not have the necessary permissions to access this site.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'superapp/base.html')

def loggingOut(request) -> HttpResponseRedirect:
    logout(request)
    return redirect('superapp:superHome')
