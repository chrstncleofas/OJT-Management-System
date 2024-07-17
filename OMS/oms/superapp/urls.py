from superapp import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

app_name = 'superapp'

urlpatterns = [
    path('', views.superHome, name='superHome'),
    path('superLogin', views.superAdminLogin, name='superLogin'),
    path('loggingOut/', views.loggingOut, name='loggingOut'),
    path('superAdminDashboard/', views.superAdminDashboard, name='superAdminDashboard'),
    path('mainDashboard', views.mainDashboard, name='mainDashboard'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
