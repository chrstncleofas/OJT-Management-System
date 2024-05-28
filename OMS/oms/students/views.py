from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from students.models import TableStudents, TimeLog
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from students.forms import StudentRegistrationForm, UserForm, ChangePasswordForm, TimeLogForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

def studentHome(request) -> HttpResponse:
    return render(request, 'students/student-base.html')

def studentDashboard(request) -> HttpResponse:
    return render(request, 'students/student-dashboard.html')


@login_required
def mainDashboard(request) -> HttpResponse:
    user = request.user
    student = get_object_or_404(TableStudents, user=user)
    firstName = student.Firstname
    lastName = student.Lastname
    return render(
        request,
        'students/student-main-dashboard.html',
        {
            'firstName': firstName,
            'lastName': lastName,
        }
    )

def TimeInAndTimeOut(request):
    user = request.user
    student = get_object_or_404(TableStudents, user=user)

    if request.method == 'POST':
        form = TimeLogForm(request.POST, request.FILES)
        if form.is_valid():
            time_log = form.save(commit=False)
            time_log.student = student
            time_log.duration = 0
            time_log.timestamp = timezone.now()
            time_log.save()
            messages.success(request, f'Time {time_log.action} recorded successfully with image.')
            return redirect('students:TimeInAndTimeOut')
        else:
            messages.error(request, 'Failed to record time. Please ensure the form is filled out correctly.')
    else:
        form = TimeLogForm()

    firstName = student.Firstname
    lastName = student.Lastname
    time_logs = TimeLog.objects.filter(student=student).order_by('-timestamp')

    return render(
        request,
        'students/timeIn-timeOut.html',
        {
            'firstName': firstName,
            'lastName': lastName,
            'time_logs': time_logs,
            'form': form,
        }
    )

def studentProfile(request):
    user = request.user
    student = get_object_or_404(TableStudents, user=user)
    
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

        messages.success(request, 'Profile updated successfully.')
        return redirect('students:profile')

    return render(
        request,
        'students/student-profile.html',
        {
            'firstName': student.Firstname,
            'lastName': student.Lastname,
            'email': student.Email,
            'course': student.Course,
            'year': student.Year,
        }
    )

def changePassword(request):
    user = request.user
    student = get_object_or_404(TableStudents, user=user)
    firstName = student.Firstname
    lastName = student.Lastname
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']            
            if check_password(current_password, user.password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('students:changePassword')
            else:
                messages.error(request, 'Your current password was entered incorrectly. Please enter it again.')
    else:
        form = ChangePasswordForm()
    
    return render(
        request,
        'students/changePassword.html',
        {
            'form': form,
            'firstName': firstName,
            'lastName': lastName,

        }
    )

def studentRegister(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentRegistrationForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.StudentID = student_form.cleaned_data['StudentID']
            student.Email = user.email
            student.Username = user.username
            student.Password = user.password
            student.save()     
            messages.success(request, 'Registration successful. Waiting for admin approval.')
            return render(request, 'students/success.html', {'message': 'Registration successful!'})
    else:
        user_form = UserForm()
        student_form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'user_form': user_form, 'student_form': student_form})

def studentLogin(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(request, username=username, password=password)
        if user:
            try:
                student = TableStudents.objects.get(user=user)
                if not student.is_approved:
                    messages.warning(request, 'Your account is not approved yet. Please wait for admin approval.')
                    return render(request, 'students/login.html')
                else:
                    if user.is_active:
                        login(request, user)
                        return redirect('students:studentPage')
                    else:
                        messages.error(request, 'Your account is disabled.')
            except TableStudents.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'students/login.html')

def success(request):
    return render(request, 'students/success.html')

def loginSuccess(request):
    return render(request, 'students/loginSuccess.html')

def studentLogout(request) -> HttpResponseRedirect:
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect(reverse('students:home'))
