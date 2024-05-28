from django.db import models
from app.models import CustomUser

class TableStudents(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    StudentID = models.CharField(max_length=10, unique=True)
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Course = models.CharField(max_length=100)
    Year = models.IntegerField()
    Username = models.CharField(max_length=100, unique=True)
    Password = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Firstname} {self.Lastname}"


class TimeLog(models.Model):
    student = models.ForeignKey(TableStudents, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('IN', 'Time In'), ('OUT', 'Time Out')])
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='time_logs/', blank=True, null=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.action} at {self.timestamp}"

