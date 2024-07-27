from typing import Union
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from students.forms import EditStudentForm
from .forms import CustomPasswordChangeForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from students.models import Tablestudent, TimeLog
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from app.models import CustomUser, AnnouncementTable
from django.views.decorators.http import require_POST
from app.forms import EditProfileForm, AnnouncementForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
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
            if user.is_staff and not user.is_superuser:
                login(request, user)
                return render(request, 'app/loginSuccess.html', {'message': 'Login successful!'})
            else:
                messages.error(request, 'You do not have the necessary permissions to access this site.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'app/base.html')

def approve_student(request, id):
    student = Tablestudent.objects.get(id=id)
    student.status = 'approved'
    student.save()

    # Send approval email
    subject = 'Your OJT Management System Account Has Been Approved'
    message = render_to_string('students/approval_email.txt', {
        'first_name': student.Firstname,
        'last_name': student.Lastname,
    })
    recipient_list = [student.Email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

    messages.success(request, f'{student.Firstname} {student.Lastname} has been approved.')
    return redirect(reverse('studentManagement'))

def reject_students(request, id):
    student = Tablestudent.objects.get(id=id)
    student.status = 'rejected'
    student.save()

    # Send email notification
    subject = 'Account Rejected'
    message = render_to_string('students/rejection_email.txt', {
        'first_name': student.Firstname,
        'last_name': student.Lastname,
    })
    recipient_list = [student.Email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

    messages.success(request, f'{student.Firstname} {student.Lastname} has been rejected.')
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

    paired_logs = []  # List to hold the paired logs

    i = 0
    while i < len(time_logs):
        if time_logs[i].action == 'IN':
            if i + 1 < len(time_logs) and time_logs[i + 1].action == 'OUT':
                paired_logs.append((time_logs[i], time_logs[i + 1]))
                work_period = time_logs[i + 1].timestamp - time_logs[i].timestamp
                if work_period > timedelta(hours=1):
                    work_period -= timedelta(hours=1)
                daily_total += work_period
                i += 1  # Skip the next log since it is already paired
        i += 1

    total_work_seconds = daily_total.total_seconds()
    total_hours = total_work_seconds / 3600

    remaining_hours = required_hours - total_hours

    context = {
        'paired_logs': paired_logs,
        'total_hours': total_hours,
        'required_hours': required_hours,
        'remaining_hours': remaining_hours,
        'firstName': firstName,
        'lastName': lastName
    }

    return render(request, 'app/TimeLogs.html', context)


def viewStudentInformation(request, student_id):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    try:
        student = Tablestudent.objects.get(pk=student_id)
    except Tablestudent.DoesNotExist:
        return HttpResponse('Student not found', status=404)
    return render(
        request, 'app/student-view-page.html', 
        {
            'student': student,
            'firstName': firstName,
            'lastName': lastName
        }
    )

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
            return redirect('listOfAnnouncement')
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

def editStudentDetails(request, studentID):
    student = get_object_or_404(Tablestudent, pk=studentID)
    user = request.user
    # 
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    # 
    if request.method == 'POST':
        form = EditStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student details updated successfully.')
            return redirect('studentManagement')
    else:
        form = EditStudentForm(instance=student)

    return render(request, 'app/edit-student.html', {
        'form': form,
        'student': student,
        'firstName': firstName,
        'lastName': lastName,
    })

@login_required
@require_POST
def archivedStudent(request, studentID):
    admin_username = request.POST.get('username')
    admin_password = request.POST.get('password')
    admin_user = authenticate(username=admin_username, password=admin_password)
    
    if admin_user and admin_user.is_staff:
        student = get_object_or_404(Tablestudent, pk=studentID)
        student.archivedStudents = 'archive'
        student.save()
        return JsonResponse({'status': 'success', 'message': f'{student.Firstname} {student.Lastname} has been archived.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Incorrect username or password.'}, status=401)

def deleteAnnouncement(request, id):
    announcement = get_object_or_404(AnnouncementTable, id=id)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Announcement has been deleted successfully.')
        return redirect('listOfAnnouncement')
    return render(request, 'app/delete-announcement.html', {'announcement': announcement})