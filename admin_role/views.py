from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import department, faculty, hod, leave, Schedule
from employees.models import leaveapplication
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, time, timedelta
from django.utils import timezone
import pytz

# Create your views here.

def index(request):
    faculty_count = faculty.objects.count()
    hod_count = hod.objects.count()
    department_count = department.objects.count()
    leave_count = leave.objects.count()
    leave_applications = leaveapplication.objects.all()
    context = {
        'faculty_count': faculty_count,
        'hod_count': hod_count,
        'department_count': department_count,
        'leave_count': leave_count,
        'leave_applications': leave_applications,
    }
    return render(request, 'index.html', context)

def faculties(request):
    faculties = faculty.objects.all()
    departments = department.objects.all()
    return render(request, 'faculties.html', {'faculties': faculties, 'departments': departments})

def add_faculty(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id', '').strip()
        faculty_name = request.POST.get('faculty_name', '').strip()
        email_id = request.POST.get('email_id', '').strip()
        subject = request.POST.get('subject', '').strip()
        department_id = request.POST.get('department_id', '').strip()
        
        if not department_id:
            messages.error(request, 'Please select a department.')
            return redirect('faculties')
        
        department_obj = department.objects.get(id=department_id)
        
        if faculty.objects.filter(faculty_id=faculty_id).exists():
            messages.error(request, 'Faculty already exists')
        else:
            faculty.objects.create(faculty_id=faculty_id, faculty_name=faculty_name, email_id=email_id, subject=subject, department=department_obj)
            return redirect('faculties')
    return redirect('faculties')

def delete_faculty(request, pk):
    delete_it = faculty.objects.get(id=pk)
    delete_it.delete()
    return redirect('faculties')

def edit_faculty(request, pk):
    edit_it = get_object_or_404(faculty, id=pk)  
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id', '').strip()
        faculty_name = request.POST.get('faculty_name', '').strip()
        email_id = request.POST.get('email_id', '').strip()
        subject = request.POST.get('subject', '').strip()
        department_id = request.POST.get('department_id', '').strip()
        
        if not department_id:
            messages.error(request, 'Please select a department.')
            return redirect('faculties')
        
        department_obj = department.objects.get(id=department_id)
        
        # Check if faculty_id already exists but is not the same faculty
        if faculty.objects.filter(faculty_id=faculty_id).exclude(id=pk).exists():
            messages.error(request, 'Faculty already exists')
        else:
            edit_it.faculty_id = faculty_id
            edit_it.faculty_name = faculty_name
            edit_it.email_id = email_id
            edit_it.subject = subject
            edit_it.department = department_obj
            edit_it.save()
            messages.success(request, 'Faculty updated successfully!')
            return redirect('faculties')  

def hods(request):
    hods = hod.objects.all()
    departments = department.objects.all()
    return render(request, 'hod.html', {'hods': hods, 'departments': departments})

def add_hod(request):
    if request.method == 'POST':
        hod_id = request.POST.get('hod_id', '').strip()
        hod_name = request.POST.get('hod_name', '').strip()
        email_id = request.POST.get('email_id', '').strip()
        subject = request.POST.get('subject', '').strip()
        department_id = request.POST.get('department_id', '').strip()
        
        if not department_id:
            messages.error(request, 'Please select a department.')
            return redirect('hod')
        
        department_obj = department.objects.get(id=department_id)
        
        if hod.objects.filter(hod_id=hod_id).exists():
            messages.error(request, 'HOD already exists')
        else:
            hod.objects.create(hod_id=hod_id, hod_name=hod_name, email_id=email_id, subject=subject, department=department_obj)
            return redirect('hods')
    return redirect('hods')

def delete_hod(request, pk):
    delete_it = hod.objects.get(id=pk)
    delete_it.delete()
    return redirect('hods')

def edit_hod(request, pk):
    edit_it = get_object_or_404(hod, id=pk)  
    if request.method == 'POST':
        hod_id = request.POST.get('hod_id', '').strip()
        hod_name = request.POST.get('hod_name', '').strip()
        email_id = request.POST.get('email_id', '').strip()
        subject = request.POST.get('subject', '').strip()
        department_id = request.POST.get('department_id', '').strip()
        
        if not department_id:
            messages.error(request, 'Please select a department.')
            return redirect('hods')
        
        department_obj = department.objects.get(id=department_id)
        
        # Check if faculty_id already exists but is not the same faculty
        if hod.objects.filter(hod_id=hod_id).exclude(id=pk).exists():
            messages.error(request, 'HOD already exists')
        else:
            edit_it.hod_id = hod_id
            edit_it.hod_name = hod_name
            edit_it.email_id = email_id
            edit_it.subject = subject
            edit_it.department = department_obj
            edit_it.save()
            messages.success(request, 'HOD updated successfully!')
            return redirect('hods')  

def departments(request):
    departments = department.objects.all()
    return render(request, 'departments.html', {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        department_name = request.POST.get('department_name', '').strip()
        num_of_subjects = request.POST.get('num_of_subjects', '')
        try:
            num_of_subjects = int(num_of_subjects) if num_of_subjects else 0
        except ValueError:
            return HttpResponse("Error: Number of Subjects must be a valid integer.")
        if department.objects.filter(department_name=department_name).exists():
            messages.error(request, 'Department already exists')
        else:
            department.objects.create(department_name=department_name, num_of_subjects=num_of_subjects)
            return redirect('departments')

def delete_department(request, pk):
    delete_it = department.objects.get(id=pk)
    delete_it.delete()
    return redirect('departments')

def edit_department(request, pk):
    edit_it = get_object_or_404(department, id=pk)  
    if request.method == 'POST':
        department_name = request.POST.get('department_name', '').strip()
        num_of_subjects = request.POST.get('num_of_subjects', '').strip()

        # Convert num_of_subjects to integer safely
        num_of_subjects = int(num_of_subjects) if num_of_subjects.isdigit() else 0

        # Check if department name already exists but is not the same department
        if department.objects.filter(department_name=department_name).exclude(id=pk).exists():
            messages.error(request, 'Department already exists')
        else:
            edit_it.department_name = department_name
            edit_it.num_of_subjects = num_of_subjects
            edit_it.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('departments') 

    return render(request, 'edit_department.html', {'edit_it': edit_it})

# def subjects(request, department_id=None):
#     if department_id:
#         subjects = subject.objects.filter(department_id=department_id)
#         department_name = department.objects.get(id=department_id).department_name
#     else:
#         subjects = subject.objects.all()
#         department_name = "All Departments"
#     return render(request, 'subjects.html', {'subjects': subjects, 'department_name': department_name})

# def add_subject(request):
#     if request.method == 'POST':
#         subject_name = request.POST.get('subject_name', '').strip()
        
#         if not subject_name:
#             messages.error(request, 'Please enter a subject name.')
#             return redirect('subjects')
        
#         if subject.objects.filter(subject_name=subject_name).exists():
#             messages.error(request, 'Subject already exists.')
#         else:
#             new_subject = subject(subject_name=subject_name)
#             new_subject.save()
#             messages.success(request, 'Subject added successfully!')
        
#         return redirect('subjects')
    
#     return render(request, 'subjects.html')

# def delete_subject(request, pk):
#     delete_it = subject.objects.get(id=pk)
#     delete_it.delete()
#     return redirect('subjects')

# def edit_subject(request, pk):
#     edit_it = get_object_or_404(subject, id=pk)  # Ensures department exists
#     if request.method == 'POST':
#         subject_name = request.POST.get('subject_name', '').strip()

#         # Check if department name already exists but is not the same department
#         if subject.objects.filter(subject_name=subject_name).exclude(id=pk).exists():
#             messages.error(request, 'Subject already exists')
#         else:
#             edit_it.subject_name = subject_name
#             edit_it.save()
#             messages.success(request, 'Subject updated successfully!')
#             return redirect('subjects')  # Redirect to department listing page

#     return render(request, 'edit_subject.html', {'edit_it': edit_it})

def schedules_list(request):
    # Get all faculty members 
    faculties = faculty.objects.all()
    
    # Get all leave applications
    leave_applications = leaveapplication.objects.all()
    
    # Get all schedules
    schedules = Schedule.objects.all()
    
    # Create a dictionary to store faculty schedules
    faculty_schedules = {}
    
    # Map schedule dates to faculties (using faculty_id as key)
    for schedule in schedules:
        if schedule.faculty:
            if schedule.faculty.faculty_id not in faculty_schedules:
                faculty_schedules[schedule.faculty.faculty_id] = schedule.start_time.date()
    
    # Default to showing all data
    filtered_type = request.GET.get('filter_type', 'all')
    
    context = {
        'faculties': faculties,
        'leave_applications': leave_applications,
        'filtered_type': filtered_type,
        'faculty_schedules': faculty_schedules
    }
    
    return render(request, 'schedules_list.html', context)

def schedules(request, faculty_id):
    faculty_obj = get_object_or_404(faculty, id=faculty_id)
    
    # Get regular schedules where this faculty is the primary faculty
    regular_schedules = Schedule.objects.filter(faculty=faculty_obj, is_replacement=False)
    
    # Get schedules where this faculty has been replaced
    replacement_schedules = Schedule.objects.filter(replaced_faculty=faculty_obj)
    
    # Get schedules where this faculty is replacing someone else
    faculty_as_replacement = Schedule.objects.filter(faculty=faculty_obj, is_replacement=True)
    
    # Combine all schedules
    all_schedules = list(regular_schedules) + list(replacement_schedules) + list(faculty_as_replacement)
    
    # Get active leaves for this faculty
    active_leaves = leaveapplication.objects.filter(
        employee_id=faculty_obj.faculty_id,
        status='Approved'
    )
    
    # Get all events for this faculty
    events = []
    
    # Add regular schedules
    for schedule in regular_schedules:
        event = {
            "id": str(schedule.id),
            "title": schedule.section_name,
            "start": schedule.start_time.isoformat(),
            "end": schedule.end_time.isoformat(),
            "className": "regular-schedule",
            "extendedProps": {
                "faculty_id": faculty_obj.id,
                "faculty_name": faculty_obj.faculty_name,
                "isReplacement": False
            }
        }
        events.append(event)
    
    # Add replacement schedules (someone is covering for this faculty)
    for schedule in replacement_schedules:
        event = {
            "id": str(schedule.id),
            "title": f"{schedule.section_name} (Replaced by {schedule.faculty.faculty_name})",
            "start": schedule.start_time.isoformat(),
            "end": schedule.end_time.isoformat(),
            "className": "replacement-schedule",
            "backgroundColor": "#dc3545",  # Bootstrap danger color
            "extendedProps": {
                "faculty_id": schedule.faculty.id,
                "faculty_name": schedule.faculty.faculty_name,
                "isReplacement": True,
                "replacedFacultyId": faculty_obj.id,
                "replacedFacultyName": faculty_obj.faculty_name
            }
        }
        events.append(event)
    
    # Add schedules where this faculty is replacing someone else
    for schedule in faculty_as_replacement:
        event = {
            "id": str(schedule.id),
            "title": f"{schedule.section_name} (Replacing {schedule.replaced_faculty.faculty_name})",
            "start": schedule.start_time.isoformat(),
            "end": schedule.end_time.isoformat(),
            "className": "faculty-as-replacement",
            "backgroundColor": "#28a745",  # Bootstrap success color
            "extendedProps": {
                "faculty_id": faculty_obj.id,
                "faculty_name": faculty_obj.faculty_name,
                "isReplacement": True,
                "replacingFacultyId": schedule.replaced_faculty.id,
                "replacingFacultyName": schedule.replaced_faculty.faculty_name
            }
        }
        events.append(event)
    
    # Convert events list to JSON string
    events_json = json.dumps(events)
    
    # Get all faculty members (for dropdown in case of manually assigning replacements)
    all_faculties = faculty.objects.exclude(id=faculty_obj.id)
    
    return render(request, 'schedules.html', {
        'schedules': all_schedules,
        'faculty': faculty_obj,
        'faculty_id': faculty_id,
        'events': events_json,
        'faculties': all_faculties,
        'active_leaves': active_leaves
    })

@csrf_exempt
def create_schedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            section_name = data.get('section_name')
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            faculty_id = data.get('faculty_id')
            
            # Validate inputs
            if not all([section_name, start_time, end_time, faculty_id]):
                return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
            # Convert strings to datetime objects
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
            
            # Get faculty object
            faculty_obj = get_object_or_404(faculty, id=faculty_id)
            
            # Check for conflicting schedules
            conflicts = Schedule.objects.filter(
                faculty=faculty_obj,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            
            if conflicts.exists():
                return JsonResponse({
                    'success': False, 
                    'error': 'This time slot conflicts with an existing schedule'
                }, status=400)
            
            # Create the schedule
            schedule = Schedule.objects.create(
                section_name=section_name,
                start_time=start_time,
                end_time=end_time,
                faculty=faculty_obj,
                is_replacement=False,
                replaced_faculty=None
            )
            
            return JsonResponse({
                'success': True,
                'id': schedule.id,
                'section_name': schedule.section_name,
                'start': schedule.start_time.isoformat(),
                'end': schedule.end_time.isoformat()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def get_schedules(request, faculty_id):
    # Get the faculty object
    faculty_obj = get_object_or_404(faculty, id=faculty_id)
    
    # Get schedules for this faculty (both regular and replacement schedules)
    regular_schedules = Schedule.objects.filter(faculty=faculty_obj, is_replacement=False)
    
    # Get schedules where this faculty has been replaced (someone else is covering for them)
    replacement_schedules = Schedule.objects.filter(replaced_faculty=faculty_obj)
    
    # Get schedules where this faculty is replacing someone else
    faculty_as_replacement = Schedule.objects.filter(faculty=faculty_obj, is_replacement=True)
    
    # Check if faculty is on leave currently
    on_leave = False
    current_leave = None
    leave_applications = leaveapplication.objects.filter(
        employee_id=faculty_obj.faculty_id,
        status='Approved'
    )
    
    # Check if any leave period overlaps with today
    today = datetime.now().date()
    for leave_app in leave_applications:
        if leave_app.from_date and leave_app.to_date:
            if leave_app.from_date <= today <= leave_app.to_date:
                on_leave = True
                current_leave = leave_app
                break
    
    events = []

    # Add regular schedules
    for schedule in regular_schedules:
        print(f"Regular Schedule: id={schedule.id}, name={schedule.section_name}, start={schedule.start_time}, end={schedule.end_time}")
        
        # Check if this schedule has a replacement (if faculty is on leave)
        has_replacement = False
        replacement_info = None
        
        if on_leave:
            replacement = Schedule.objects.filter(
                replaced_faculty=faculty_obj,
                is_replacement=True,
                start_time=schedule.start_time,
                end_time=schedule.end_time
            ).first()
            
            if replacement:
                has_replacement = True
                replacement_info = {
                    "faculty_id": replacement.faculty.id,
                    "faculty_name": replacement.faculty.faculty_name,
                    "department": replacement.faculty.department.department_name if replacement.faculty.department else ""
                }
        
        event = {
            "id": str(schedule.id),
            "title": schedule.section_name,
            "start": schedule.start_time.isoformat(),
            "end": schedule.end_time.isoformat(),
            "className": "regular-schedule",
            "extendedProps": {
                "faculty_id": faculty_obj.id,
                "faculty_name": faculty_obj.faculty_name,
                "isReplacement": False,
                "onLeave": on_leave,
                "hasReplacement": has_replacement,
                "replacementInfo": replacement_info
            }
        }
        events.append(event)
    
    # Add replacement schedules (someone is covering for this faculty)
    for schedule in replacement_schedules:
        print(f"Replacement Schedule: id={schedule.id}, name={schedule.section_name}, start={schedule.start_time}, end={schedule.end_time}")
        
        event = {
            "id": str(schedule.id),
            "title": f"{schedule.section_name} (Replaced by {schedule.faculty.faculty_name})",
            "start": schedule.start_time.isoformat(),
            "end": schedule.end_time.isoformat(),
            "className": "replacement-schedule",
            "backgroundColor": "#dc3545",  # Bootstrap danger color
            "extendedProps": {
                "faculty_id": schedule.faculty.id,
                "faculty_name": schedule.faculty.faculty_name,
                "replacementId": schedule.id, 
                "isReplacement": True,
                "replacedFacultyId": faculty_obj.id,
                "replacedFacultyName": faculty_obj.faculty_name,
                "onLeave": on_leave,
                "leaveInfo": {
                    "from_date": current_leave.from_date.isoformat() if current_leave and current_leave.from_date else None,
                    "to_date": current_leave.to_date.isoformat() if current_leave and current_leave.to_date else None,
                    "leave_type": current_leave.leave_type if current_leave else None
                } if current_leave else None
            }
        }
        events.append(event)
    
    # Add schedules where this faculty is replacing someone else
    for schedule in faculty_as_replacement:
        print(f"Faculty as Replacement: id={schedule.id}, name={schedule.section_name}, start={schedule.start_time}, end={schedule.end_time}")
        
        event = {
            "id": str(schedule.id),
            "title": f"{schedule.section_name} (Replacing {schedule.replaced_faculty.faculty_name})",
            "start": schedule.start_time.isoformat(),
            "end": schedule.end_time.isoformat(),
            "className": "faculty-as-replacement",
            "backgroundColor": "#28a745",  # Bootstrap success color
            "extendedProps": {
                "faculty_id": faculty_obj.id,
                "faculty_name": faculty_obj.faculty_name,
                "isReplacement": True,
                "replacingFacultyId": schedule.replaced_faculty.id,
                "replacingFacultyName": schedule.replaced_faculty.faculty_name,
                "originalScheduleInfo": {
                    "section_name": schedule.section_name,
                    "department": schedule.replaced_faculty.department.department_name if schedule.replaced_faculty.department else ""
                }
            }
        }
        events.append(event)

    print(f"Returning {len(events)} events")  # Debug print
    return JsonResponse(events, safe=False)

@csrf_exempt
def update_schedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            schedule_id = data.get('id')
            section_name = data.get('section_name')
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            
            # Validate inputs
            if not all([schedule_id, section_name, start_time, end_time]):
                return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
            
            # Get schedule object
            schedule = get_object_or_404(Schedule, id=schedule_id)
            
            # Don't allow editing replacement schedules
            if schedule.is_replacement:
                return JsonResponse({'success': False, 'error': 'Cannot edit replacement schedules'}, status=400)
            
            # Convert strings to datetime objects
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
            
            # Check for conflicting schedules (excluding the current schedule)
            conflicts = Schedule.objects.filter(
                faculty=schedule.faculty,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(id=schedule_id)
            
            if conflicts.exists():
                return JsonResponse({
                    'success': False, 
                    'error': 'This time slot conflicts with another schedule'
                }, status=400)
            
            # Update the schedule
            schedule.section_name = section_name
            schedule.start_time = start_time
            schedule.end_time = end_time
            schedule.save()
            
            # Update any associated replacement schedules
            replacements = Schedule.objects.filter(replaced_faculty=schedule.faculty, is_replacement=True)
            for replacement in replacements:
                if (replacement.start_time == schedule.start_time and 
                    replacement.end_time == schedule.end_time):
                    replacement.section_name = section_name
                    replacement.save()
            
            return JsonResponse({
                'success': True,
                'id': schedule.id,
                'section_name': schedule.section_name,
                'start': schedule.start_time.isoformat(),
                'end': schedule.end_time.isoformat()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_schedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            schedule_id = data.get('id')
            
            if not schedule_id:
                return JsonResponse({'success': False, 'error': 'Missing schedule ID'}, status=400)
            
            # Get schedule object
            schedule = get_object_or_404(Schedule, id=schedule_id)
            
            # Don't allow deleting replacement schedules directly
            if schedule.is_replacement:
                return JsonResponse({'success': False, 'error': 'Cannot delete replacement schedules directly'}, status=400)
            
            # Get any associated replacement schedules and delete them first
            replacements = Schedule.objects.filter(
                replaced_faculty=schedule.faculty,
                is_replacement=True,
                start_time=schedule.start_time,
                end_time=schedule.end_time
            )
            
            for replacement in replacements:
                replacement.delete()
            
            # Delete the schedule
            schedule.delete()
            
            return JsonResponse({'success': True})
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
def clear_schedules(request, faculty_id):
    if request.method == 'POST':
        try:
            # Get faculty
            faculty_obj = get_object_or_404(faculty, id=faculty_id)
            
            # Get all schedules for this faculty (both regular and replacements)
            regular_schedules = Schedule.objects.filter(faculty=faculty_obj)
            
            # Also delete schedules where this faculty is being replaced
            replacement_schedules = Schedule.objects.filter(replaced_faculty=faculty_obj)
            
            # Count total schedules deleted
            count_regular = regular_schedules.count()
            count_replacements = replacement_schedules.count()
            
            # Delete all schedules
            regular_schedules.delete()
            replacement_schedules.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'All schedules cleared successfully. {count_regular} regular schedules and {count_replacements} replacement schedules were deleted.'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@csrf_exempt
def allocate_replacements(request):
    """
    Automatically allocate replacements for faculty who are on leave
    """
    if request.method == "POST":
        try:
            # Get leave applications that are approved and have valid dates
            leave_applications = leaveapplication.objects.filter(
                status='Approved',
                from_date__isnull=False,
                to_date__isnull=False
            )
            
            print(f"Found {leave_applications.count()} approved leave applications with valid dates")
            
            replacements_created = 0
            
            for leave_app in leave_applications:
                # Find the faculty who is on leave
                try:
                    print(f"Processing leave for employee ID: {leave_app.employee_id}, "
                          f"from {leave_app.from_date} to {leave_app.to_date}")
                    
                    faculty_on_leave = faculty.objects.get(faculty_id=leave_app.employee_id)
                    print(f"Found faculty: {faculty_on_leave.faculty_name}")
                    
                    # Get all schedules for the faculty on leave for the leave period
                    leave_start = leave_app.from_date
                    leave_end = leave_app.to_date
                    
                    # Debug info about dates
                    print(f"Leave period: {leave_start} to {leave_end}")
                    
                    # Use timezone-aware datetime objects for comparison
                    leave_start_dt = timezone.make_aware(datetime.combine(leave_start, time.min))
                    leave_end_dt = timezone.make_aware(datetime.combine(leave_end, time.max))
                    
                    # Find schedules that fall within the leave period 
                    schedules_to_replace = Schedule.objects.filter(
                        faculty=faculty_on_leave,
                        is_replacement=False,  # Only consider regular schedules
                        start_time__lte=leave_end_dt,  # Schedule starts before or on leave end
                        end_time__gte=leave_start_dt   # Schedule ends after or on leave start
                    )
                    
                    print(f"Found {schedules_to_replace.count()} schedules to replace")
                    
                    # For each schedule, find a faculty who is free during that time
                    for schedule in schedules_to_replace:
                        print(f"Processing schedule: {schedule.section_name} from {schedule.start_time} to {schedule.end_time}")
                        
                        # Check if a replacement already exists
                        existing_replacement = Schedule.objects.filter(
                            is_replacement=True,
                            replaced_faculty=faculty_on_leave,
                            start_time=schedule.start_time,
                            end_time=schedule.end_time
                        ).exists()
                        
                        if existing_replacement:
                            print(f"Replacement already exists for this schedule")
                            continue
                        
                        # Get all faculties except the one on leave
                        available_faculties = faculty.objects.exclude(id=faculty_on_leave.id)
                        
                        # Filter out faculties who already have a schedule during this time
                        busy_faculties = []
                        for potential_faculty in available_faculties:
                            overlapping = Schedule.objects.filter(
                                faculty=potential_faculty,
                                start_time__lt=schedule.end_time,
                                end_time__gt=schedule.start_time
                            ).exists()
                            
                            if overlapping:
                                busy_faculties.append(potential_faculty.id)
                        
                        # Get available faculties
                        available_faculties = available_faculties.exclude(id__in=busy_faculties)
                        
                        if available_faculties.exists():
                            # Select the first available faculty
                            replacement_faculty = available_faculties.first()
                            print(f"Assigning {replacement_faculty.faculty_name} as replacement")
                            
                            # Create a replacement schedule
                            replacement = Schedule(
                                section_name=schedule.section_name,
                                start_time=schedule.start_time,
                                end_time=schedule.end_time,
                                faculty=replacement_faculty,
                                is_replacement=True,
                                replaced_faculty=faculty_on_leave
                            )
                            replacement.save()
                            replacements_created += 1
                            print(f"Created replacement schedule: {replacement.id}")
                        else:
                            print("No available faculty found for replacement")
                            
                except faculty.DoesNotExist:
                    # Skip if the employee is not a faculty member
                    print(f"No faculty found with ID {leave_app.employee_id}")
                    continue
                except Exception as e:
                    print(f"Error processing leave application {leave_app.id}: {str(e)}")
            
            return JsonResponse({
                "success": True, 
                "message": f"Replacement schedules allocated successfully. Created {replacements_created} replacements."
            })
            
        except Exception as e:
            print(f"Error in allocate_replacements: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def leaves(request):
    leaves = leave.objects.all()
    return render(request, 'leave_types.html', {'leaves': leaves})

def add_leave(request):
    if request.method == 'POST':
        leave_name = request.POST.get('leave_name', '').strip()
        
        if not leave_name:
            messages.error(request, 'Please enter a leave name.')
            return redirect('leaves')
        
        if leave.objects.filter(leave_name=leave_name).exists():
            messages.error(request, 'Leave already exists.')
        else:
            new_leave = leave(leave_name=leave_name)
            new_leave.save()
            messages.success(request, 'Leave added successfully!')
        
        return redirect('leaves')
    
    return render(request, 'leave_types.html')

def delete_leave(request, pk):
    delete_it = leave.objects.get(id=pk)
    delete_it.delete()
    return redirect('leaves')

def edit_leave(request, pk):
    edit_it = get_object_or_404(leave, id=pk)  
    if request.method == 'POST':
        leave_name = request.POST.get('leave_name', '').strip()

        # Check if department name already exists but is not the same department
        if leave.objects.filter(leave_name=leave_name).exclude(id=pk).exists():
            messages.error(request, 'Leave already exists')
        else:
            edit_it.leave_name = leave_name
            edit_it.save()
            messages.success(request, 'leave updated successfully!')
            return redirect('leaves')  

    return render(request, 'edit_leave.html', {'edit_it': edit_it})

def leave_applications(request):
    """
    View to display and manage leave applications for admin users
    """
    applications = leaveapplication.objects.all().order_by('-created_at')
    
    context = {
        'applications': applications
    }
    
    return render(request, 'leave_applications.html', context)

@csrf_exempt
def update_leave_status(request, pk):
    """
    Update the status of a leave application
    """
    if request.method == "POST":
        try:
            leave_app = get_object_or_404(leaveapplication, pk=pk)
            data = json.loads(request.body)
            new_status = data.get('status')
            
            if new_status not in ['Pending', 'Approved', 'Rejected']:
                return JsonResponse({"error": "Invalid status"}, status=400)
            
            # Update the status
            leave_app.status = new_status
            leave_app.save()
            
            # If approved, check if we need to allocate replacements
            replacements_created = 0
            if new_status == 'Approved':
                # Find the faculty who is on leave
                try:
                    faculty_on_leave = faculty.objects.get(faculty_id=leave_app.employee_id)
                    print(f"Faculty on leave: {faculty_on_leave.faculty_name}")
                    
                    # Get all schedules for the faculty on leave for the leave period
                    leave_start = leave_app.from_date
                    leave_end = leave_app.to_date
                    
                    if leave_start and leave_end:
                        print(f"Leave period: {leave_start} to {leave_end}")
                        
                        # Convert to datetime for comparison with timezone awareness
                        leave_start_dt = timezone.make_aware(datetime.combine(leave_start, time.min))
                        leave_end_dt = timezone.make_aware(datetime.combine(leave_end, time.max))
                        
                        # Find schedules that fall within the leave period
                        schedules_to_replace = Schedule.objects.filter(
                            faculty=faculty_on_leave,
                            is_replacement=False,
                            start_time__gte=leave_start_dt,
                            end_time__lte=leave_end_dt
                        )
                        
                        print(f"Found {schedules_to_replace.count()} schedules to replace")
                        
                        # Get a list of all faculty members from the same department
                        same_dept_faculties = faculty.objects.filter(
                            department=faculty_on_leave.department
                        ).exclude(id=faculty_on_leave.id)
                        
                        other_dept_faculties = faculty.objects.exclude(
                            department=faculty_on_leave.department
                        ).exclude(id=faculty_on_leave.id)
                        
                        # Combine both lists with same department faculties first
                        potential_replacements = list(same_dept_faculties) + list(other_dept_faculties)
                        
                        # For each schedule, find a faculty who is free during that time
                        for schedule in schedules_to_replace:
                            print(f"Processing schedule: {schedule.section_name} from {schedule.start_time} to {schedule.end_time}")
                            
                            # Check if a replacement already exists
                            existing_replacement = Schedule.objects.filter(
                                is_replacement=True,
                                replaced_faculty=faculty_on_leave,
                                start_time=schedule.start_time,
                                end_time=schedule.end_time
                            ).exists()
                            
                            if existing_replacement:
                                print(f"Replacement already exists for this schedule, skipping")
                                continue
                            
                            # Find an available faculty for replacement with most similar subject expertise
                            replacement_faculty = None
                            
                            for potential_faculty in potential_replacements:
                                # Check if this faculty is available during this time slot
                                overlapping = Schedule.objects.filter(
                                    faculty=potential_faculty,
                                    start_time__lt=schedule.end_time,
                                    end_time__gt=schedule.start_time
                                ).exists()
                                
                                # Check if the faculty is also on leave during this period
                                faculty_on_leave_too = leaveapplication.objects.filter(
                                    employee_id=potential_faculty.faculty_id,
                                    status='Approved',
                                    from_date__lte=schedule.start_time.date(),
                                    to_date__gte=schedule.start_time.date()
                                ).exists()
                                
                                # Prioritize faculty who teach the same subject
                                if not overlapping and not faculty_on_leave_too:
                                    # If faculty teaches the same subject, prioritize them
                                    if potential_faculty.subject == faculty_on_leave.subject:
                                        replacement_faculty = potential_faculty
                                        print(f"Found available faculty with matching subject: {replacement_faculty.faculty_name}")
                                        break
                                    # Otherwise, keep them as a candidate
                                    elif replacement_faculty is None:
                                        replacement_faculty = potential_faculty
                            
                            if replacement_faculty:
                                # Create a replacement schedule
                                replacement = Schedule(
                                    section_name=schedule.section_name,
                                    start_time=schedule.start_time,
                                    end_time=schedule.end_time,
                                    faculty=replacement_faculty,
                                    is_replacement=True,
                                    replaced_faculty=faculty_on_leave
                                )
                                replacement.save()
                                replacements_created += 1
                                print(f"Created replacement schedule: {replacement.id} with faculty {replacement_faculty.faculty_name}")
                            else:
                                print("No available faculty found for replacement")
                
                except faculty.DoesNotExist:
                    # Skip if the employee is not a faculty member
                    print(f"No faculty found with ID {leave_app.employee_id}")
                except Exception as e:
                    print(f"Error allocating replacements: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
            return JsonResponse({
                "success": True, 
                "message": f"Leave application status updated to {new_status}",
                "replacements_created": replacements_created
            })
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def create_replacement(request):
    """
    Manually create a replacement schedule for a faculty
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            schedule_id = data.get('schedule_id')
            replacement_faculty_id = data.get('replacement_faculty_id')
            
            if not schedule_id or not replacement_faculty_id:
                return JsonResponse({"error": "Missing required parameters"}, status=400)
            
            # Get the original schedule
            original_schedule = get_object_or_404(Schedule, id=schedule_id)
            
            # Get the replacement faculty
            replacement_faculty = get_object_or_404(faculty, id=replacement_faculty_id)
            
            # Check if this faculty is available during this time slot
            overlapping = Schedule.objects.filter(
                faculty=replacement_faculty,
                start_time__lt=original_schedule.end_time,
                end_time__gt=original_schedule.start_time
            ).exists()
            
            if overlapping:
                return JsonResponse({
                    "error": "This faculty already has a schedule during this time. Please choose a different faculty."
                }, status=400)
            
            # Check if a replacement already exists
            existing_replacement = Schedule.objects.filter(
                is_replacement=True,
                replaced_faculty=original_schedule.faculty,
                start_time=original_schedule.start_time,
                end_time=original_schedule.end_time
            ).exists()
            
            if existing_replacement:
                return JsonResponse({
                    "error": "A replacement already exists for this schedule."
                }, status=400)
            
            # Create a replacement schedule
            replacement = Schedule(
                section_name=original_schedule.section_name,
                start_time=original_schedule.start_time,
                end_time=original_schedule.end_time,
                faculty=replacement_faculty,
                is_replacement=True,
                replaced_faculty=original_schedule.faculty
            )
            replacement.save()
            
            # Return the new replacement schedule
            return JsonResponse({
                "id": replacement.id,
                "title": f"{replacement.section_name} (Replacing {replacement.replaced_faculty.faculty_name})",
                "start": replacement.start_time.isoformat(),
                "end": replacement.end_time.isoformat(),
                "faculty_id": replacement_faculty.id,
                "faculty_name": replacement_faculty.faculty_name,
                "replaced_faculty_id": original_schedule.faculty.id,
                "replaced_faculty_name": original_schedule.faculty.faculty_name
            })
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_active_leaves(request, faculty_id):
    """
    API endpoint to get active leaves for a faculty member
    """
    try:
        # Get the faculty
        faculty_obj = get_object_or_404(faculty, id=faculty_id)
        
        # Get all approved leave applications for this faculty
        leaves = leaveapplication.objects.filter(
            employee_id=faculty_obj.faculty_id,
            status='Approved'
        )
        
        # Filter to only include current or future leaves
        today = datetime.now().date()
        active_leaves = []
        
        for leave in leaves:
            if leave.to_date and leave.to_date >= today:
                # Get replacements for this leave
                replacements = Schedule.objects.filter(
                    replaced_faculty=faculty_obj,
                    is_replacement=True,
                    start_time__date__gte=leave.from_date,
                    end_time__date__lte=leave.to_date
                )
                
                # Count replacements
                replacement_count = replacements.count()
                
                # Get regular schedules that might need replacements
                regular_schedules = Schedule.objects.filter(
                    faculty=faculty_obj,
                    is_replacement=False
                )
                
                # Count schedules that fall within leave period
                # This is a simplified count that doesn't consider exact day matching
                schedule_count = 0
                for schedule in regular_schedules:
                    # Check if this is a recurring schedule that would fall in the leave period
                    weekday = schedule.start_time.weekday()
                    
                    # Calculate how many occurrences of this weekday fall within the leave period
                    days = (leave.to_date - leave.from_date).days + 1
                    occurrences = days // 7
                    if occurrences > 0 or weekday == leave.from_date.weekday():
                        schedule_count += 1
                
                active_leaves.append({
                    'id': leave.id,
                    'leave_type': leave.leave_type,
                    'from_date': leave.from_date.isoformat() if leave.from_date else None,
                    'to_date': leave.to_date.isoformat() if leave.to_date else None,
                    'status': leave.status,
                    'replacements': {
                        'assigned': replacement_count,
                        'needed': schedule_count,
                        'is_fully_covered': replacement_count >= schedule_count
                    }
                })
        
        return JsonResponse(active_leaves, safe=False)
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


