from app import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logoutView, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('timeSheet', views.timeSheet, name='timeSheet'),
    # 
    path('viewTimeLogs/<int:student_id>/', views.viewTimeLogs, name='viewTimeLogs'),
    path('viewStudentInformation/<int:student_id>/', views.viewStudentInformation, name='viewStudentInformation'),
    # 
    path('changePass', views.changePass, name='changePass'),
    path('mainDashboard', views.mainDashboard, name='mainDashboard'),
    path('studentManagement', views.studentManagement, name='studentManagement'),
    path('editStudentDetails/<int:studentID>/', views.editStudentDetails, name='editStudentDetails'),
    # 
    path('approve_student/<int:id>/', views.approve_student, name='approve_student'),
    path('reject_students/<int:id>/', views.reject_students, name='reject_students'),
    # 
    path('archivedStudent/<int:studentID>/', views.archivedStudent, name='archivedStudent'),
    path('get_admin_password_hash/', views.get_admin_password_hash, name='get_admin_password_hash'),
    path('unArchivedStudent/<int:id>/', views.unArchivedStudent, name='unArchivedStudent'),
    # 
    path('getAllPendingRegister', views.getAllPendingRegister, name='getAllPendingRegister'),
    path('getListOfApproveStudent', views.getListOfApproveStudent, name='getListOfApproveStudent'),
    path('getListOfArchivedStudents', views.getListOfArchivedStudents, name='getListOfArchivedStudents'),
    # 
    path('announcement', views.announcement, name='announcement'),
    path('listOfAnnouncement', views.listOfAnnouncement, name='listOfAnnouncement'),
    path('editAnnouncement/<int:id>/', views.editAnnouncement, name='editAnnouncement'),
    path('deleteAnnouncement/<int:id>/', views.deleteAnnouncement, name='deleteAnnouncement'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
