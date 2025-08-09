from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Schedule, Subject
from django.http import HttpRequest
from django.db.models import Count
import uuid

# Schedule List View
def schedule_list(request):
    """Display list of all schedules"""
    schedules = Schedule.objects.all().order_by('-updated_at')
    
    # Add subjects count for each schedule
    for schedule in schedules:
        schedule.subjects_count = Subject.objects.filter(schedule=schedule).count()
        schedule.created_at = schedule.updated_at  # Use updated_at as created_at
        schedule.status = 'public' if schedule.public else 'private'
    
    context = {
        'schedules': schedules,
    }
    return render(request, 'schedule/scheduleList.html', context)

# Create your views here.
def schedule(request, id):
    context = {
        'id': id,
        'weekdays': [
            (1, 'Thứ 2'),
            (2, 'Thứ 3'),
            (3, 'Thứ 4'),
            (4, 'Thứ 5'),
            (5, 'Thứ 6'),
            (6, 'Thứ 7'),
            (7, 'Chủ Nhật'),
        ],
        'periods': [
            (1, '07:00 - 07:50'),
            (2, '08:00 - 08:50'),
            (3, '09:00 - 09:50'),
            (4, '10:00 - 10:50'),
            (5, '11:00 - 11:50'),
            (6, '12:30 - 13:20'),
            (7, '13:30 - 14:20'),
            (8, '14:30 - 15:20'),
            (9, '15:30 - 16:20'),
            (10, '16:30 - 17:20'),
            (11, '17:30 - 18:15'),
            (12, '18:15 - 19:10'),
            (13, '19:10 - 19:55'),
            (14, '19:55 - 20:40'),
        ],
        'schedules': Subject.objects.filter(schedule__scheduleID=id),
    }
    return render(request, 'schedule/editor.html', context)

@csrf_exempt
def add_schedule(request):
    if request.method == 'POST':
        print(request.POST)
        subject = Subject.objects.create(
            subject_id=str(uuid.uuid4()),
            subject_name=request.POST.get('subject_name'),
            subject_code=request.POST.get('subject_code'),
            schedule=Schedule.objects.get(scheduleID=request.POST.get('schedule_id')),
            room=request.POST.get('room', ''),
            teacher=request.POST.get('teacher', ''),
            weekday=int(request.POST.get('weekday', 1)),
            start_period=int(request.POST.get('start_period', 1)),
            end_period=int(request.POST.get('end_period', 2)),
            color=request.POST.get('color', '#000000')  # Default color if not provided
        )
        subject.save()

    return redirect('edit', id=request.POST.get('schedule_id'))

@csrf_exempt
def delete_schedule(request, id, subject_id):
    if request.method == 'POST':
        subject = Subject.objects.get(subject_id=subject_id)
        subject.delete()
        return redirect('edit', id=id)
    return JsonResponse({'status': 'error'})

def create_schedule(request:HttpRequest):
    # Logic to create a schedule
    if (request.user == None): return
    print("Creating schedule...")
    sche = Schedule.objects.create(title="New Schedule", scheduleID=str(uuid.uuid4()), user=request.user)
    sche.save()
    return redirect('edit', id=sche.scheduleID)

def schedule_export(request, id):
    """Render fixed-size schedule export page"""
    context = {
        'id': id,
        'weekdays': [
            (1, 'Thứ 2'),
            (2, 'Thứ 3'),
            (3, 'Thứ 4'),
            (4, 'Thứ 5'),
            (5, 'Thứ 6'),
            (6, 'Thứ 7'),
            (7, 'Chủ Nhật'),
        ],
        'periods': [
            (1, '07:00 - 07:50'),
            (2, '08:00 - 08:50'),
            (3, '09:00 - 09:50'),
            (4, '10:00 - 10:50'),
            (5, '11:00 - 11:50'),
            (6, '12:30 - 13:20'),
            (7, '13:30 - 14:20'),
            (8, '14:30 - 15:20'),
            (9, '15:30 - 16:20'),
            (10, '16:30 - 17:20'),
            (11, '17:30 - 18:15'),
            (12, '18:15 - 19:10'),
            (13, '19:10 - 19:55'),
            (14, '19:55 - 20:40'),
        ],
        'schedules': Subject.objects.filter(schedule__scheduleID=id)
    }
    return render(request, 'schedule/schedule_export.html', context)

@csrf_exempt
def delete_schedule_list(request, id):
    """Delete a schedule from the list"""
    if request.method == 'POST':
        try:
            schedule = get_object_or_404(Schedule, scheduleID=id)
            # Delete all subjects associated with this schedule
            Subject.objects.filter(schedule=schedule).delete()
            # Delete the schedule
            schedule.delete()
            return redirect('schedule_list')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})