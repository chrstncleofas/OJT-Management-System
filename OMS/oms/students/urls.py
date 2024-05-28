from students import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

app_name = 'students'

urlpatterns = [
    path('', views.studentHome, name='home'),
    path('login', views.studentLogin, name='login'),
    path('register/', views.studentRegister, name='register'),
    path('dashboard/', views.studentDashboard, name='dashboard'),
    path('studentPage/', views.mainDashboard, name='studentPage'),
    path('TimeInAndTimeOut/', views.TimeInAndTimeOut, name='TimeInAndTimeOut'),
    path('profile/', views.studentProfile, name='profile'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('logout/', views.studentLogout, name='logout'),
    path('success/', views.success, name='success'),
    path('loginSuccess/', views.loginSuccess, name='loginSuccess'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
