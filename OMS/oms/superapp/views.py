from typing import Union
from datetime import timedelta
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from superapp.forms import SuperuserForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from students.models import Tablestudent, TimeLog
from app.models import CustomUser, AnnouncementTable
from app.forms import EditProfileForm, AnnouncementForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
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
    approve = Tablestudent.objects.filter(status='approved')
    approve_count = approve.count()
    # Pending
    pending = Tablestudent.objects.filter(status='pending')
    pending_count = pending.count()
    # Rejected
    reject = Tablestudent.objects.filter(status='rejected')
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
