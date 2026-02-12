from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.contrib.auth.models import User
from authapp.models import College, Event, AppUser, Registration
from .models import Complaint

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()

@login_required
@user_passes_test(is_admin)
def admin_overview(request):
    total_colleges = College.objects.count()
    total_events = Event.objects.count()
    total_registrations = Registration.objects.count()
    pending_complaints = Complaint.objects.filter(status='OPEN').count()
    
    # Chart Data: Events by Type
    event_counts = Event.objects.values('event_type__name').annotate(count=Count('id'))
    chart_labels = [item['event_type__name'] for item in event_counts]
    chart_data = [item['count'] for item in event_counts]
    
    context = {
        'total_colleges': total_colleges,
        'total_events': total_events,
        'total_registrations': total_registrations,
        'pending_complaints': pending_complaints,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'appadmin/overview.html', context)

@login_required
@user_passes_test(is_admin)
def admin_events(request):
    events = Event.objects.select_related('department__college', 'event_type').all().order_by('-created_at')
    return render(request, 'appadmin/events.html', {'events': events})

@login_required
@user_passes_test(is_admin)
def admin_colleges(request):
    if request.method == 'POST':
        college_id = request.POST.get('college_id')
        action = request.POST.get('action')
        college = get_object_or_404(College, id=college_id)
        
        if action == 'accept':
            college.verification_status = 'ACCEPTED'
            college.is_active = True
            # Update associated College Admin users
            AppUser.objects.filter(college=college, role='COLLEGE_ADMIN').update(verification_status='ACCEPTED')
            User.objects.filter(appuser__college=college, appuser__role='COLLEGE_ADMIN').update(is_active=True)
            
        elif action == 'reject':
            college.verification_status = 'REJECTED'
            college.is_active = False
            # Update associated College Admin users
            AppUser.objects.filter(college=college, role='COLLEGE_ADMIN').update(verification_status='REJECTED')
            User.objects.filter(appuser__college=college, appuser__role='COLLEGE_ADMIN').update(is_active=False)
            
        college.save()
        return redirect('admin_colleges')
        
    colleges = College.objects.all().order_by('-created_at')
    return render(request, 'appadmin/colleges.html', {'colleges': colleges})

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    # Fetch all AppUsers except superusers if they have AppUser profiles, 
    # or generally just all AppUsers.
    users = AppUser.objects.select_related('auth_user', 'college', 'department').all().order_by('-id')
    return render(request, 'appadmin/requests.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_complaints(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        action = request.POST.get('action')
        
        if action == 'resolve':
            complaint = get_object_or_404(Complaint, id=complaint_id)
            complaint.status = 'RESOLVED'
            complaint.save()
            return redirect('admin_complaints')
            
    complaints = Complaint.objects.select_related('user').all().order_by('-created_at')
    return render(request, 'appadmin/complaints.html', {'complaints': complaints})

def admin_payments(request):
    return render(request, 'appadmin/payments.html')
