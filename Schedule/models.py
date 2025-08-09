from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Schedule(models.Model):
    title = models.CharField(max_length=100)
    scheduleID = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='owner')
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Subject(models.Model):
    subject_id = models.CharField(max_length=32, unique=True, default='None')
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=32)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='subjects')
    room = models.CharField(max_length=50, blank=True)
    teacher = models.CharField(max_length=100, blank=True)
    weekday = models.IntegerField(default=1)
    start_period = models.IntegerField(default=1)
    end_period = models.IntegerField(default=2)
    color = models.CharField(max_length=10, default="#000")
    def __str__(self):
        return self.name
