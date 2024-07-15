from datetime import timedelta
from typing import Union
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from app.models import CustomUser, AnnouncementTable
from app.forms import EditProfileForm, AnnouncementForm
from django.contrib import messages
from students.models import Tablestudent, TimeLog
from django.core.mail import send_mail
from app.forms import CustomUserCreationForm
from .forms import CustomPasswordChangeForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

HOME_URL_PATH = 'app/base.html'
DASHBOARD = 'app/dashboard.html'
MAIN_DASHBOARD = 'app/main-dashboard.html'
MANAGEMENT_STUDENT = 'app/manage-student.html'
ANNOUNCEMENT = 'app/announcement.html'
LIST_ANNOUNCEMENT = 'app/list-announcement.html'
PROFILE = 'app/profile.html'
CHANGE_PASSWORD = 'app/changePassword.html'

def home(request) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse]:        
    return render(request, HOME_URL_PATH)

def dashboard(request) -> HttpResponse:
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

def profile(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=admin)
    return render(request, PROFILE, {
        'form': form,
        'firstName': firstName,
        'lastName': lastName
    })

def changePass(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name   
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changePass')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, CHANGE_PASSWORD, {
        'form': form,
        'firstName': firstName,
        'lastName': lastName
    })

def getAllPendingRegister(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    # 
    students = Tablestudent.objects.filter(is_approved=False)
    return render(request, MANAGEMENT_STUDENT, {
        'getAllPendingRegister': students,
        'firstName': firstName,
        'lastName': lastName
    })

def studentManagement(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    # 
    firstName = admin.first_name
    lastName = admin.last_name
    # 
    approved = Tablestudent.objects.filter(status='approved')
    pending = Tablestudent.objects.filter(status='pending')
    rejected = Tablestudent.objects.filter(status='rejected')
    # 
    archive = Tablestudent.objects.filter(archivedStudents='archive')

    return render(
        request,
        MANAGEMENT_STUDENT,
        {
            'getListOfApproveStudent': approved,
            'getAllPendingRegister': pending,
            'getAllRejectedApplication': rejected,
            'getListOfArchivedStudents': archive,
            'firstName': firstName,
            'lastName': lastName
        }
    )

def getListOfApproveStudent(request):
    students = Tablestudent.objects.filter(is_approved=True)
    return render(request, MANAGEMENT_STUDENT, {
        'getListOfApproveStudent': students,
    })

def getListOfArchivedStudents(request):
    students = Tablestudent.objects.filter(archivedStudents='archive')
    return render(request, MANAGEMENT_STUDENT, {
        'getListOfArchivedStudents': students,
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_staff:
                login(request, user)
                return render(request, 'app/loginSuccess.html', {'message': 'Login successful!'})
            else:
                messages.error(request, 'You do not have the necessary permissions to access this site.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'app/base.html')

def register(request):
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
            return render(request, 'app/success.html', {'message': 'Registration successful!'})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def editStudents(request):
    user = request.user
    student = get_object_or_404(Tablestudent, user=user)
    
    if request.method == 'POST':
        firstName = request.POST.get('Firstname')
        lastName = request.POST.get('Lastname')
        email = request.POST.get('Email')
        course = request.POST.get('Course')
        year = request.POST.get('Year')

        student.Firstname = firstName
        student.Lastname = lastName
        student.Email = email
        student.Course = course
        student.Year = year
        student.save()

        messages.success(request, 'Student successfuly updated...')
        return redirect('studentManagement')

    return render(
        request,
        'app/edit-student.html',
        {
            'firstName': student.Firstname,
            'lastName': student.Lastname,
            'email': student.Email,
            'course': student.Course,
            'year': student.Year,
        }
    )

def approve_student(request, id):
    student = Tablestudent.objects.get(id=id)
    student.status = 'approved'
    student.save()
    messages.success(request, f'{student.Firstname} {student.Lastname} has been approved.')
    return redirect(reverse('studentManagement'))

def reject_students(request, id):
    student = Tablestudent.objects.get(id=id)
    student.status = 'rejected'
    student.save()
    messages.success(request, f'{student.Firstname} {student.Lastname} has been rejected.')
    return redirect(reverse('studentManagement'))

def archivedStudent(request):
    if request.method == 'POST':
        admin_password = request.POST.get('admin_password')
        student_id = request.POST.get('student_id')
        user = request.user

        # Authenticate admin
        admin_user = authenticate(username=user.username, password=admin_password)
        if admin_user and admin_user.is_staff:
            student = get_object_or_404(Tablestudent, id=student_id)
            student.archivedStudents = 'archive'
            student.save()
            messages.success(request, f'{student.Firstname} {student.Lastname} has been archived.')
        else:
            messages.error(request, 'Incorrect password. Please try again.')

    return redirect(reverse('studentManagement'))

def unArchivedStudent(request, id):
    student = Tablestudent.objects.get(id=id)
    student.archivedStudents = 'unarchive'
    student.save()
    messages.success(request, f'{student.Firstname} {student.Lastname} has been remove to archived.')
    return redirect(reverse('studentManagement'))

def logoutView(request) -> HttpResponseRedirect:
    logout(request)
    return redirect(home)

def is_admin(user):
    user_admin = user.is_superuser
    user_staff = user.is_staff
    return user_admin or user_staff

@user_passes_test(is_admin)
def timeSheet(request):
    students = Tablestudent.objects.all()
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    return render(
        request,
        'app/timeSheet.html',
        {
            'students': students,
            'firstName': firstName,
            'lastName': lastName
        }
    )

def viewTimeLogs(request, student_id):
    student = get_object_or_404(Tablestudent, id=student_id)
    firstName = student.Firstname
    lastName = student.Lastname
    time_logs = []
    total_hours = 0
    required_hours = 600

    selected_student = get_object_or_404(Tablestudent, id=student_id)
    time_logs = TimeLog.objects.filter(student=selected_student).order_by('timestamp')

    total_work_seconds = 0
    daily_start = None
    daily_total = timedelta()

    for log in time_logs:
        if log.action == 'IN':
            daily_start = log.timestamp
        elif log.action == 'OUT' and daily_start:
            work_period = log.timestamp - daily_start
            if work_period > timedelta(hours=1):
                work_period -= timedelta(hours=1)
            daily_total += work_period
            daily_start = None

    total_work_seconds = daily_total.total_seconds()
    total_hours = total_work_seconds / 3600

    remaining_hours = required_hours - total_hours
    
    context = {
        'time_logs': time_logs,
        'total_hours': total_hours,
        'required_hours': required_hours,
        'remaining_hours': remaining_hours,
        'firstName': firstName,
        'lastName': lastName
    }

    return render(request, 'app/TimeLogs.html', context)

def viewStudentInformation(request, student_id):
    try:
        student = Tablestudent.objects.get(pk=student_id)
    except Tablestudent.DoesNotExist:
        return HttpResponse('Student not found', status=404)
    return render(request, 'app/student-view-page.html', {'student': student})

def listOfAnnouncement(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    announcements = AnnouncementTable.objects.all()
    return render(request, LIST_ANNOUNCEMENT, {
        'listOfAnnouncement': announcements,
        'firstName': firstName,
        'lastName': lastName
    })

def announcement(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement has been added successfully.')
            return redirect('announcement')
    else:
        form = AnnouncementForm()
    return render(request, ANNOUNCEMENT,
        {
            'form': form,
            'firstName': firstName,
            'lastName': lastName
        }
    )

def editAnnouncement(request, id):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name

    announcement = get_object_or_404(AnnouncementTable, id=id)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement has been updated successfully.')
            return redirect('listOfAnnouncement')
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'app/edit-announcement.html', {
        'form': form,
        'firstName': firstName,
        'lastName': lastName,
        'announcement': announcement,
    })

