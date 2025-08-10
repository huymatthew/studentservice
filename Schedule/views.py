from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Schedule, Subject
from django.http import HttpRequest
from django.db.models import Count
import uuid
import json

def schedule_list(request):
    """Display list of all schedules"""
    if (request.user is None): return redirect('login')
    schedules = Schedule.objects.filter(user=request.user).order_by('-updated_at')
    
    for schedule in schedules:
        schedule.subjects_count = Subject.objects.filter(schedule=schedule).count()
        schedule.created_at = schedule.updated_at 
        schedule.status = 'public' if schedule.public else 'private'
        
        sw = Subject.objects.filter(schedule=schedule).values('weekday')
        schedule.sw = [False] * 7
        for item in sw:
            schedule.sw[item['weekday'] - 1] = True
    context = {
        'schedules': schedules,
    }
    return render(request, 'schedule/scheduleList.html', context)

def schedule(request, id):
    schedule, created = Schedule.objects.get_or_create(
        scheduleID=id,
        defaults={'title': 'Thời khóa biểu mới'}
    )
    
    context = {
        'id': id,
        'schedule': schedule,
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
def edit_subject(request):
    """Edit an existing subject"""
    if request.method == 'POST':
        try:
            subject_id = request.POST.get('subject_id')
            schedule_id = request.POST.get('schedule_id')
            
            # Get the subject to edit
            subject = get_object_or_404(Subject, subject_id=subject_id)
            
            # Update subject fields
            subject.subject_name = request.POST.get('subject_name')
            subject.subject_code = request.POST.get('subject_code')
            subject.room = request.POST.get('room', '')
            subject.teacher = request.POST.get('teacher', '')
            subject.weekday = int(request.POST.get('weekday', 1))
            subject.start_period = int(request.POST.get('start_period', 1))
            subject.end_period = int(request.POST.get('end_period', 2))
            subject.color = request.POST.get('color', '#4171c9')
            # Note: Skip note field as it's not in the model
            
            subject.save()
            
            return redirect('edit', id=schedule_id)
            
        except Exception as e:
            print(f"Error editing subject: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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
            Subject.objects.filter(schedule=schedule).delete()
            schedule.delete()
            return redirect('schedule_list')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def update_schedule_title(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            schedule_id = data.get('schedule_id')
            new_title = data.get('title', '').strip()
            
            if not schedule_id or not new_title:
                return JsonResponse({'success': False, 'message': 'Thiếu thông tin bắt buộc'})
            
            if len(new_title) > 100:
                return JsonResponse({'success': False, 'message': 'Tên thời khóa biểu không được quá 100 ký tự'})
            
            schedule = Schedule.objects.filter(scheduleID=schedule_id).first()

            if schedule:
                print("Updating schedule title...")
                schedule.title = new_title
                schedule.save()
            else:
                return JsonResponse({'success': False, 'message': 'Không tìm thấy thời khóa biểu với ID đã cho'})
            
            return JsonResponse({
                'success': True, 
                'message': 'Đã cập nhật tên thời khóa biểu thành công',
                'title': new_title
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Dữ liệu không hợp lệ'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Phương thức không được hỗ trợ'})