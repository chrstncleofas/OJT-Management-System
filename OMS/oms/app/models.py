from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    position = models.CharField(max_length=100)

class Announcement(models.Model):
    Title = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='announcement/', blank=True, null=True)
    Category = models.CharField(max_length=150, blank=True, null=True)
    Date = models.DateField()
    Description = models.CharField(max_length=450)
    Status = models.CharField(max_length=100)
