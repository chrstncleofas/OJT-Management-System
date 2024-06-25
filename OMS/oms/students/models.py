from django.db import models
from app.models import CustomUser

class Tablestudents(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    StudentID = models.CharField(max_length=10, unique=True)
    Firstname = models.CharField(max_length=100)
    Middlename = models.CharField(max_length=100, blank=True, null=True)
    Lastname = models.CharField(max_length=100)   
    Prefix = models.CharField(max_length=100, blank=True, null=True)  
    Email = models.EmailField(unique=True)
    Number = models.CharField(max_length=100)
    Course = models.CharField(max_length=100)
    Year = models.CharField(max_length=50)
    Image = models.ImageField(upload_to='profileImage/', blank=True, null=True)
    Username = models.CharField(max_length=100, unique=True)
    Password = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"{self.Firstname} {self.Lastname}"

class TimeLog(models.Model):
    student = models.ForeignKey(Tablestudents, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('IN', 'Time In'), ('OUT', 'Time Out')])
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='time_logs/', blank=True, null=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.action} at {self.timestamp}"

