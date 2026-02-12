from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

from django.contrib import messages
from django.db.models import Count
from django.utils.timezone import now
from authapp.models import AppUser, Department, Event, Registration, Course, Degree

@never_cache
@login_required
def dashboard(request):
    return render(request, "college_admin/dashboard/dashboard.html")

@never_cache
@login_required
def events_registry(request):
    return render(request, "college_admin/dashboard/events_registry.html")

@never_cache
@login_required
def analytics(request):
    college = request.user.appuser.college
    
    # Chart 1: Top 5 Events by Registrations
    top_events = (
        Event.objects.filter(department__college=college)
        .annotate(reg_count=Count('subevent__registration'))
        .order_by('-reg_count')[:5]
    )
    event_labels = [e.title for e in top_events]
    event_data = [e.reg_count for e in top_events]

    # Chart 2: Registrations per Department
    dept_stats = (
        Department.objects.filter(college=college)
        .annotate(reg_count=Count('event__subevent__registration'))
        .order_by('-reg_count')
    )
    dept_labels = [d.name for d in dept_stats]
    dept_data = [d.reg_count for d in dept_stats]

    return render(request, "college_admin/dashboard/analytics.html", {
        "event_labels": event_labels,
        "event_data": event_data,
        "dept_labels": dept_labels,
        "dept_data": dept_data,
    })

@never_cache
@login_required
def settings(request):
    return render(request, "college_admin/dashboard/settings.html")

@never_cache
@login_required
def department_admins(request):
    college = request.user.appuser.college

    # ADD DEPARTMENT ADMIN
    if request.method == "POST":
        department_id = request.POST.get("department")
        name = request.POST.get("admin_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        first_name, *last_name = name.split(" ")

        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=" ".join(last_name),
            password=password,
            is_active=True
        )

        user.groups.add(Group.objects.get(name='department admin'))

        AppUser.objects.create(
            auth_user=user,
            role="DEPT_ADMIN",
            phone=phone,
            college=college,
            department_id=department_id,
            verification_status="ACCEPTED"
        )

        return redirect("college_admin:department_admins")

    # FETCH DEPARTMENT ADMINS
    dept_admins = AppUser.objects.select_related(
        "auth_user", "department"
    ).filter(
        role="DEPT_ADMIN",
        college=college
    )

    departments = Department.objects.filter(college=college)

    context = {
        "dept_admins": dept_admins,
        "departments": departments
    }

    return render(
        request,
        "college_admin/dashboard/dept_admins.html",
        context
    )

@never_cache
@login_required
def toggle_department_admin(request, user_id):
    app_user = get_object_or_404(AppUser, id=user_id)
    app_user.auth_user.is_active = not app_user.auth_user.is_active
    app_user.auth_user.save()
    return redirect("college_admin:department_admins")

@never_cache
@login_required
def events_registry(request):
    college = request.user.appuser.college
    current_year = now().year

    events = Event.objects.filter(
        department__college=college,
        start_date__year=current_year
    ).prefetch_related("subevent_set")

    return render(
        request,
        "college_admin/dashboard/events_registry.html",
        {
            "events": events,
            "current_year": current_year
        }
    )

@never_cache
@login_required
def college_admin_profile(request):
    user = request.user
    app_user = user.appuser

    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        app_user.phone = request.POST.get("phone")
        current = request.POST.get("current_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")

        if current or new or confirm:
            if not user.check_password(current):
                messages.error(request, "Current password is incorrect")
            elif new != confirm:
                messages.error(request, "New passwords do not match")
            else:
                user.set_password(new)
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully")
        user.save()
        app_user.save()

        return redirect("college_admin:college_admin_profile")

    return render(
        request,
        "college_admin/profile.html",
        {
            "user_obj": user,
            "app_user": app_user
        }
    )

@never_cache
@login_required
def college_admin_dashboard(request):
    college = request.user.appuser.college
    current_year = now().year

    total_events = Event.objects.filter(
        department__college=college
    ).count()

    total_departments = Department.objects.filter(
        college=college
    ).count()

    total_registrations = Registration.objects.filter(
        sub_event__event__department__college=college
    ).count()

    latest_events = Event.objects.filter(
        department__college=college
    ).order_by("-created_at")[:5]

    registration_chart = (
        Event.objects.filter(
            department__college=college
        )
        .annotate(reg_count=Count("subevent__registration"))
        .order_by("-reg_count")[:5]
    )

    context = {
        "total_events": total_events,
        "total_departments": total_departments,
        "total_registrations": total_registrations,
        "latest_events": latest_events,
        "chart_labels": [e.title for e in registration_chart],
        "chart_data": [e.reg_count for e in registration_chart],
    }

    return render(
        request,
        "college_admin/dashboard/dashboard.html",
        context
    )
from appadmin.models import Complaint

@never_cache
@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "college_admin/dashboard/complaints.html", {"complaints": complaints})

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
        return redirect("college_admin:my_complaints")
    return redirect("college_admin:my_complaints")


@never_cache
@login_required
def manage_courses(request):
    college = request.user.appuser.college
    departments = Department.objects.filter(college=college).prefetch_related('course_set__degree')
    degrees = Degree.objects.all()

    return render(request, "college_admin/dashboard/manage_courses.html", {
        "departments": departments,
        "degrees": degrees
    })


@never_cache
@login_required
def add_course(request):
    if request.method == "POST":
        department_id = request.POST.get("department")
        degree_id = request.POST.get("degree")
        name = request.POST.get("name")
        duration = request.POST.get("duration")

        try:
            department = Department.objects.get(id=department_id, college=request.user.appuser.college)
            degree = Degree.objects.get(id=degree_id)
            
            Course.objects.create(
                department=department,
                degree=degree,
                name=name,
                duration_years=duration
            )
            messages.success(request, "Course added successfully")
        except Exception as e:
            messages.error(request, f"Error adding course: {e}")
            
    return redirect("college_admin:manage_courses")


@never_cache
@login_required
def edit_course(request, course_id):
    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id, department__college=request.user.appuser.college)
        degree_id = request.POST.get("degree")
        name = request.POST.get("name")
        duration = request.POST.get("duration")

        try:
            course.degree = Degree.objects.get(id=degree_id)
            course.name = name
            course.duration_years = duration
            course.save()
            messages.success(request, "Course updated successfully")
        except Exception as e:
            messages.error(request, f"Error updating course: {e}")

    return redirect("college_admin:manage_courses")


@never_cache
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, department__college=request.user.appuser.college)
    course.delete()
    messages.success(request, "Course deleted successfully")
    return redirect("college_admin:manage_courses")


@never_cache
@login_required
def manage_departments(request):
    college = request.user.appuser.college
    departments = Department.objects.filter(college=college).annotate(course_count=Count('course'))
    
    return render(request, "college_admin/dashboard/manage_departments.html", {
        "departments": departments
    })


@never_cache
@login_required
def add_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        college = request.user.appuser.college
        
        try:
            Department.objects.create(name=name, college=college)
            messages.success(request, "Department added successfully")
        except Exception as e:
            messages.error(request, f"Error adding department: {e}")
            
    return redirect("college_admin:manage_departments")


@never_cache
@login_required
def edit_department(request, dept_id):
    if request.method == "POST":
        college = request.user.appuser.college
        department = get_object_or_404(Department, id=dept_id, college=college)
        name = request.POST.get("name")
        
        try:
            department.name = name
            department.save()
            messages.success(request, "Department updated successfully")
        except Exception as e:
            messages.error(request, f"Error updating department: {e}")
            
    return redirect("college_admin:manage_departments")


@never_cache
@login_required
def delete_department(request, dept_id):
    college = request.user.appuser.college
    department = get_object_or_404(Department, id=dept_id, college=college)
    
    # Optional: Check if it has courses or events before deleting? 
    # For now, relying on standard cascade or behavior, but let's just delete.
    try:
        department.delete()
        messages.success(request, "Department deleted successfully")
    except Exception as e:
        messages.error(request, f"Error deleting department: {e}")
        
    return redirect("college_admin:manage_departments")



