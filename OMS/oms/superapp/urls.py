from superapp import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

app_name = 'superapp'

urlpatterns = [
    path('', views.superHome, name='home'),
    path('createSuperAccount/', views.createSuperAccount, name='createSuperAccount'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
