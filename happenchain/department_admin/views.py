
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.timezone import now

from authapp.models import AppUser, Department, Event, EventType, Registration, SubEvent

@never_cache
@login_required
def overview(request):
    admin_user = request.user
    admin_appuser = admin_user.appuser

    
    # Chart Data: Registrations per Event
    events_with_regs = (
        Event.objects.filter(
            department=admin_appuser.department,
            created_by=admin_user # Filter events created by this admin if needed, or all dept events
        )
        .annotate(reg_count=Count('subevent__registration'))
        .order_by('-reg_count')[:5]  # Top 5 events
    )

    chart_labels = [e.title for e in events_with_regs]
    chart_data = [e.reg_count for e in events_with_regs]

    return render(request, "department_admin/dashboard/overview.html", {
        "user_personal_details":admin_user,
        "user_proff_details":admin_appuser,
        "active_events": Event.objects.filter(department=admin_appuser.department).count(),
        "pending": AppUser.objects.filter(department=admin_appuser.department, verification_status='PENDING').count(),
        "registrations": Registration.objects.filter(sub_event__event__department=admin_appuser.department).count(),
        "chart_labels": chart_labels,
        "chart_data": chart_data,
    })

@never_cache
@login_required
def events(request):
    event_types = EventType.objects.all()
    current_year = now().year

    events = Event.objects.filter(
        created_by=request.user,
        department=request.user.appuser.department,
        start_date__year=current_year
    ).prefetch_related('subevent_set')

    return render(request, "department_admin/dashboard/events.html", {
            "event_types": event_types,
            "events":events,
        })

@never_cache
@login_required
def registrations(request):
    return render(request, "department_admin/dashboard/registrations.html")

@never_cache
@login_required
def analytics(request):
    return render(request, "department_admin/dashboard/analytics.html")

@never_cache
@login_required
def department_registrations(request):
    department = request.user.appuser.department

    registrations = (
        Registration.objects
        .select_related(
            "user",
            "team",
            "sub_event",
            "sub_event__event"
        )
        .filter(sub_event__event__department=department)
        .order_by("-registered_at")
    )

    return render(
        request,
        "department_admin/dashboard/registrations.html",
        {
            "registrations": registrations
        }
    )

@never_cache
@login_required
def student_registration_requests(request):
    admin_appuser = request.user.appuser

    students = (
        AppUser.objects
        .select_related("auth_user", "college", "course", "department")
        .filter(
            department=admin_appuser.department,
            college=admin_appuser.college,
            role = 'STUDENT',
        )
        .order_by("-id")
    )

    return render(
        request,
        "department_admin/dashboard/student_registrations.html",
        {
            "students": students
        }
    )

@never_cache
@login_required
def toggle_student_status(request, student_id):
    admin_appuser = request.user.appuser

    student = get_object_or_404(
        AppUser,
        id=student_id,
        department=admin_appuser.department,
        college=admin_appuser.college
    )

    with transaction.atomic():
        # Toggle active status
        student.auth_user.is_active = not student.auth_user.is_active
        student.auth_user.save()

        # Sync verification status
        if student.auth_user.is_active:
            student.verification_status = 'ACCEPTED'
        else:
            student.verification_status = 'REJECTED'

        student.save()

    return redirect("department_admin:student-registrations")

@never_cache
@login_required
def create_event(request):
    if request.method == "POST":
        title = request.POST.get("title")
        event_type_id = request.POST.get("event_type")
        venue = request.POST.get("venue")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        description = request.POST.get("description")
        event_photo = request.FILES.get("event_photo")

        # logged-in admin details
        admin_appuser = request.user.appuser

        # basic validation
        if not all([title, event_type_id, venue, start_date, end_date, description]):
            messages.error(request, "All fields are required.")
            return redirect("department_admin:dashboard-events")

        try:
            event_type = EventType.objects.get(id=event_type_id)
        except EventType.DoesNotExist:
            messages.error(request, "Invalid event type selected.")
            return redirect("department_admin:dashboard-events")

        Event.objects.create(
            title=title,
            event_type=event_type,
            venue=venue,
            start_date=start_date,
            end_date=end_date,
            description=description,
            event_photo=event_photo,
            department=admin_appuser.department,
            created_by=request.user
        )

        messages.success(request, "Event created successfully.")
        return redirect("department_admin:dashboard-events")

 
    return redirect("department_admin:dashboard-events")

@never_cache
@login_required
def create_sub_event(request):
    if request.method != "POST":
        return redirect("department_admin:dashboard-events")

    admin_appuser = request.user.appuser

    # Fetch POST data
    event_id = request.POST.get("event_id")
    title = request.POST.get("title")
    description = request.POST.get("description")
    cost = request.POST.get("cost")
    is_team_event = request.POST.get("is_team_event") == "true"
    min_team_size = request.POST.get("min_team_size")
    max_team_size = request.POST.get("max_team_size")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    venue = request.POST.get("venue")

    # Validate parent event (SECURITY IMPORTANT)
    event = get_object_or_404(
        Event,
        id=event_id,
        department=admin_appuser.department,
    )

    # Basic validation
    if not all([title, description, start_time, end_time, venue]):
        messages.error(request, "All required fields must be filled.")
        return redirect("department_admin:dashboard-events")

    # Team validation
    if is_team_event:
        if not min_team_size or not max_team_size:
            messages.error(request, "Team size is required for team events.")
            return redirect("department_admin:dashboard-events")

        if int(min_team_size) > int(max_team_size):
            messages.error(request, "Minimum team size cannot exceed maximum.")
            return redirect("department_admin:dashboard-events")
    else:
        min_team_size = None
        max_team_size = None

    # Create SubEvent safely
    with transaction.atomic():
        SubEvent.objects.create(
            event=event,
            title=title,
            description=description,
            cost=cost if cost else None,
            is_team_event=is_team_event,
            min_team_size=min_team_size,
            max_team_size=max_team_size,
            start_time=start_time,
            end_time=end_time,
            venue=venue
        )

    messages.success(request, "Sub-event created successfully.")
    return redirect("department_admin:dashboard-events")


@never_cache
@login_required
def profile(request):
    user = request.user
    appuser = user.appuser

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("department_admin:profile")

    return render(
        request,
        "department_admin/dashboard/profile.html",
        {
            "user": user,
            "appuser": appuser
        }
    )

from appadmin.models import Complaint

@never_cache
@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "department_admin/dashboard/complaints.html", {"complaints": complaints})

@never_cache
@login_required
def submit_complaint(request):
    if request.method == "POST":
        issue = request.POST.get("issue")
        against = request.POST.get("against")
        
        Complaint.objects.create(
            user=request.user,
            issue=issue,
            against=against,
            status='OPEN'
        )
        messages.success(request, "Complaint submitted successfully")
        return redirect("department_admin:my_complaints")
    return redirect("department_admin:my_complaints")


@never_cache
@login_required
def edit_event(request, event_id):
    admin_appuser = request.user.appuser
    event = get_object_or_404(
        Event, 
        id=event_id, 
        department=admin_appuser.department
    )

    if request.method == "POST":
        title = request.POST.get("title")
        event_type_id = request.POST.get("event_type")
        venue = request.POST.get("venue")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        description = request.POST.get("description")
        event_photo = request.FILES.get("event_photo")

        # Validation
        if not all([title, event_type_id, venue, start_date, end_date, description]):
            messages.error(request, "All fields are required.")
            return redirect("department_admin:dashboard-events")

        try:
            event_type = EventType.objects.get(id=event_type_id)
        except EventType.DoesNotExist:
            messages.error(request, "Invalid event type.")
            return redirect("department_admin:dashboard-events")

        # Update fields
        event.title = title
        event.event_type = event_type
        event.venue = venue
        event.start_date = start_date
        event.end_date = end_date
        event.description = description
        
        if event_photo:
            event.event_photo = event_photo

        event.save()
        messages.success(request, "Event updated successfully.")
        return redirect("department_admin:dashboard-events")

    # If GET, redirect (handling via modal only)
    return redirect("department_admin:dashboard-events")


@never_cache
@login_required
def edit_sub_event(request, sub_event_id):
    admin_appuser = request.user.appuser
    sub_event = get_object_or_404(
        SubEvent, 
        id=sub_event_id, 
        event__department=admin_appuser.department
    )

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        cost = request.POST.get("cost")
        is_team_event = request.POST.get("is_team_event") == "true"
        min_team_size = request.POST.get("min_team_size")
        max_team_size = request.POST.get("max_team_size")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        venue = request.POST.get("venue")

        if not all([title, description, start_time, end_time, venue]):
            messages.error(request, "All required fields must be filled.")
            return redirect("department_admin:dashboard-events")

        # Update fields
        sub_event.title = title
        sub_event.description = description
        sub_event.cost = cost if cost else None
        sub_event.is_team_event = is_team_event
        sub_event.venue = venue
        sub_event.start_time = start_time
        sub_event.end_time = end_time

        if is_team_event:
            if not min_team_size or not max_team_size:
                messages.error(request, "Team sizes required for team events.")
                return redirect("department_admin:dashboard-events")
            sub_event.min_team_size = min_team_size
            sub_event.max_team_size = max_team_size
        else:
            sub_event.min_team_size = None
            sub_event.max_team_size = None

        sub_event.save()
        messages.success(request, "Sub-event updated successfully.")
        return redirect("department_admin:dashboard-events")

    return redirect("department_admin:dashboard-events")
