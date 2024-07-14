from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    position = models.CharField(max_length=100)

class AnnouncementTable(models.Model):
    Title = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='announcement/', blank=True, null=True)
    Description = models.CharField(max_length=150)
    Status = models.CharField(max_length=100)
