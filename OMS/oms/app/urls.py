from app import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
# from .views import LoginView, LogoutView
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logoutView, name='logout'),
    path('register', views.register, name='register'), 
    path('dashboard', views.dashboard, name='dashboard'),
    path('timeSheet', views.timeSheet, name='timeSheet'),
    path('viewTimeLogs/<int:student_id>/', views.viewTimeLogs, name='viewTimeLogs'),
    path('changePass', views.changePass, name='changePass'),
    path('mainDashboard', views.mainDashboard, name='mainDashboard'),
    path('studentManagement', views.studentManagement, name='studentManagement'),
    path('approve_student/<int:id>/', views.approve_student, name='approve_student'),
    path('reject_students/<int:id>/', views.reject_students, name='reject_students'),
    path('getAllPendingRegister', views.getAllPendingRegister, name='getAllPendingRegister'),
    path('getListOfApproveStudent', views.getListOfApproveStudent, name='getListOfApproveStudent'),
    path('<int:id>/viewStudentInformation/', views.viewStudentInformation, name='viewStudentInformation'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
