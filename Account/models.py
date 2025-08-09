from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    pass
    
    def __str__(self):
        return f"{self.username}"

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    class_name = models.CharField(max_length=20, blank=True)
    major = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    credits_earned = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Đang học'),
        ('graduated', 'Đã tốt nghiệp'),
        ('suspended', 'Tạm nghỉ'),
        ('dropped', 'Thôi học')
    ], default='active')
    
    def __str__(self):
        return f"Profile of {self.user.username} - {self.student_id}"
