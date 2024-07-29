from django.db import models
from app.models import CustomUser

class DataTableStudents(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    ARCHIVED_STATUS = [
        ('NotArchive', 'NotArchive'),
        ('Archive', 'Archive'),
        ('UnArchive', 'Unarchive'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    StudentID = models.CharField(max_length=16, unique=True)
    Firstname = models.CharField(max_length=100)
    Middlename = models.CharField(max_length=100, blank=True, null=True)
    Lastname = models.CharField(max_length=100)   
    Prefix = models.CharField(max_length=100, blank=True, null=True)  
    Email = models.EmailField(unique=True)
    Address = models.CharField(max_length=250)
    Number = models.CharField(max_length=11)
    Course = models.CharField(max_length=100)
    Year = models.CharField(max_length=50)
    Image = models.ImageField(upload_to='profileImage/', blank=True, null=True)
    Username = models.CharField(max_length=100, unique=True)
    Password = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    archivedStudents = models.CharField(max_length=30, choices=ARCHIVED_STATUS, default='NotArchive')

    def __str__(self):
        return f"{self.Firstname} {self.Lastname}"

class TimeLog(models.Model):
    student = models.ForeignKey(DataTableStudents, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('IN', 'Time In'), ('OUT', 'Time Out')])
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='time_logs/', blank=True, null=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.action} at {self.timestamp}"

