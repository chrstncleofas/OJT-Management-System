import json
from typing import Union
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from datetime import datetime, timedelta
from django.core.mail import send_mail
from .forms import CustomPasswordChangeForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from app.models import CustomUser, Announcement
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password
from app.forms import EditProfileForm, AnnouncementForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from students.forms import EditStudentForm, ScheduleSettingForm
from students.models import DataTableStudents, TimeLog, Schedule
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
    approve = DataTableStudents.objects.filter(status='Approved', archivedStudents='NotArchive')
    approve_count = approve.count()
    # Pending
    pending = DataTableStudents.objects.filter(status='Pending')
    pending_count = pending.count()
    # Rejected
    reject = DataTableStudents.objects.filter(status='Rejected')
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

def studentManagement(request):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    # 
    firstName = admin.first_name
    lastName = admin.last_name
    # 
    approved = DataTableStudents.objects.filter(status='Approved', archivedStudents='NotArchive')
    # 
    pending = DataTableStudents.objects.filter(status='Pending')
    # 
    rejected = DataTableStudents.objects.filter(status='Rejected')
    # 
    archive = DataTableStudents.objects.filter(archivedStudents='Archive')

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

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_staff and not user.is_superuser:
                login(request, user)
                request.session['admin_password'] = user.password
                return render(request, 'app/loginSuccess.html', {'message': 'Login successful!'})
            else:
                messages.error(request, 'You do not have the necessary permissions to access this site.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'app/base.html')

@login_required
@require_POST
@csrf_exempt
def archivedStudent(request, id):
    try:
        student = DataTableStudents.objects.get(pk=id)
        student.archivedStudents = 'Archive'
        student.save()
        return JsonResponse({'status': 'success', 'message': f'{student.Firstname} {student.Lastname} has been archived.'})
    except DataTableStudents.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def get_admin_password_hash(request):
    return JsonResponse({'password': request.user.password})

@login_required
@require_POST
@csrf_exempt  # Ensure CSRF is properly handled in production
def validate_admin_password(request):
    input_password = json.loads(request.body).get('password')
    user = request.user

    if user.check_password(input_password):
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Incorrect password'})

def approve_student(request, id):
    student = DataTableStudents.objects.get(id=id)
    student.status = 'Approved'
    student.save()

    # Send approval email
    subject = 'Your OJT Management System Account Has Been Approved'
    message = render_to_string('app/approval_email.txt', {
        'first_name': student.Firstname,
        'last_name': student.Lastname,
    })
    recipient_list = [student.Email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

    messages.success(request, f'{student.Firstname} {student.Lastname} has been approved.')
    return redirect(reverse('studentManagement'))

@csrf_exempt
def reject_students(request, id):
    if request.method == 'POST':
        student = DataTableStudents.objects.get(id=id)
        data = json.loads(request.body)
        reason = data.get('reason', 'No reason provided')
        student.status = 'Rejected'
        student.save()

        # Send email notification
        subject = 'Account Rejected'
        message = render_to_string('app/rejection_email.txt', {
            'first_name': student.Firstname,
            'last_name': student.Lastname,
            'reason': reason
        })
        recipient_list = [student.Email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

def unArchivedStudent(request, id):
    student = DataTableStudents.objects.get(id=id)
    student.archivedStudents = 'UnArchive'
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
    students = DataTableStudents.objects.filter(status='Approved', archivedStudents='NotArchive')
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

def viewPendingApplication(request, id):
    students = get_object_or_404(DataTableStudents, id=id)
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    return render(
        request,
        'app/pending-view-page.html',
        {
            'students': students,
            'firstName': firstName,
            'lastName': lastName
        }
    )


def viewTimeLogs(request, student_id):
    student = get_object_or_404(DataTableStudents, id=student_id)
    firstName = student.Firstname
    lastName = student.Lastname
    time_logs = []
    total_hours = 0
    required_hours = 600

    selected_student = get_object_or_404(DataTableStudents, id=student_id)
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

    # Fetching the entire weekly schedule for the student
    full_schedule = Schedule.objects.filter(student=student, day__in=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']).order_by('id')

    context = {
        'paired_logs': paired_logs,
        'total_hours': total_hours,
        'required_hours': required_hours,
        'remaining_hours': remaining_hours,
        'firstName': firstName,
        'lastName': lastName,
        'full_schedule': full_schedule,
    }

    return render(request, 'app/TimeLogs.html', context)


def viewStudentInformation(request, student_id):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name
    try:
        student = DataTableStudents.objects.get(pk=student_id)
    except DataTableStudents.DoesNotExist:
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
    announcements = Announcement.objects.all()
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

    announcement = get_object_or_404(Announcement, id=id)

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

def setSchedule(request, id):
    user = request.user
    admin = get_object_or_404(CustomUser, id=user.id)
    firstName = admin.first_name
    lastName = admin.last_name

    student = get_object_or_404(DataTableStudents, id=id)
    current_day = datetime.now().strftime('%A')
    
    if request.method == 'POST':
        form = ScheduleSettingForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            
            Schedule.objects.create(
                student=student,
                day=day,
                start_time=start_time,
                end_time=end_time
            )
            return redirect('editStudentDetails', id=id)
    else:
        form = ScheduleSettingForm()
    
    schedule = Schedule.objects.filter(student=student).order_by('day')
    next_schedule = []
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    start_index = day_order.index(current_day)
    for i in range(start_index + 1, len(day_order)):
        next_schedule.extend(schedule.filter(day=day_order[i]))
    for i in range(0, start_index + 1):
        next_schedule.extend(schedule.filter(day=day_order[i]))

    return render(request, 'app/set-schedule.html', {
        'form': form,
        'student': student,
        'firstName': firstName,
        'lastName': lastName,
        'schedule': next_schedule,
    })

def editStudentDetails(request, id):
    student = get_object_or_404(DataTableStudents, pk=id)
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
def get_admin_password_hash(request):
    return JsonResponse({'password': request.user.password})

def deleteAnnouncement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Announcement has been deleted successfully.')
        return redirect('listOfAnnouncement')
    return render(request, 'app/delete-announcement.html', {'announcement': announcement})