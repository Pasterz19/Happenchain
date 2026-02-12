from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login ,logout
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User,Group
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.http import JsonResponse
import os

from authapp.models import AppUser, College, Course, Degree, Department


# Create your views here.
def load_departments(request):
    college_id = request.GET.get('college_id')
    departments = Department.objects.filter(college_id=college_id).order_by('name')
    return JsonResponse(list(departments.values('id', 'name')), safe=False)

def load_degrees(request):
    department_id = request.GET.get('department_id')
    # Filter degrees that have at least one course in the selected department
    degrees = Degree.objects.filter(course__department_id=department_id).distinct().order_by('name')
    return JsonResponse(list(degrees.values('id', 'name')), safe=False)

def load_courses(request):
    department_id = request.GET.get('department_id')
    degree_id = request.GET.get('degree_id')
    courses = Course.objects.filter(department_id=department_id, degree_id=degree_id).order_by('name')
    return JsonResponse(list(courses.values('id', 'name')), safe=False)

def get_home(request):
    return render(request,'authapp/home.html')

# def get_student_register(request):
#     colleges = College.objects.all()
#     degree = Degree.objects.all()
#     departments = Department.objects.all()
#     courses = Course.objects.all()
#     return render(request,'authapp/student-registration.html',{'colleges': colleges,
#             'degree': degree,
#             'departments': departments,
#             'courses':courses})

def get_college_register(request):
    return render(request,'authapp/college-registration.html')

def post_login(request):
    uname = request.POST['username'].strip().lower()
    password = request.POST['password']

    user = authenticate(username=uname,password=password)
    print(user)
    if user is None:
        messages.error(request, "Invalid username or password")
        return redirect('home')

    if user.is_superuser or user.groups.filter(name='admin').exists():
        login(request,user)
        return redirect('admin_overview')
        
    if user.groups.filter(name='user').exists():
        if user.appuser.verification_status == 'ACCEPTED':
            login(request,user)
            return redirect('appuser:user_dashboard')
        else:
            messages.warning(request, "Your account verification is pending.")
            return redirect('home')
            
    if user.groups.filter(name='college admin').exists():
        if user.appuser.verification_status == 'ACCEPTED':
            login(request,user)
            return redirect('college_admin:dashboard')
        else:
            messages.warning(request, "Your account verification is pending.")
            return redirect('home')
            
    if user.groups.filter(name='department admin').exists():
        if user.appuser.verification_status == 'ACCEPTED':
            login(request,user)
            return redirect('department_admin:dashboard-overview')
        else:
            messages.warning(request, "Your account verification is pending.")
            return redirect('home')
        
    return redirect('home')

@require_POST
def common_logout(request):
    logout(request)
    return redirect("home") 

def college_register(request):
    if request.method == "POST":

        college_name = request.POST.get("collegename")
        email = request.POST.get("college-email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        state = request.POST.get("state")
        district = request.POST.get("district")
        declaration_file = request.FILES.get("official-letter")

        if User.objects.filter(username=email).exists():
            # messages.error(request, "An account with this email already exists.")
            return redirect("college_register")
            
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )

                user.groups.add(Group.objects.get(name='college admin'))

                college = College.objects.create(
                    name=college_name,
                    email=email,
                    address=address,
                    city=district,
                    state=state,
                    declaration_document=declaration_file,
                )

                AppUser.objects.create(
                    auth_user=user,
                    phone=phone,
                    college=college,
                    role='college_admin'  # match model choices
                )

            return redirect("home")

            
            
        except Exception as e:
            print("ERROR:", e)
            return redirect("college_register")
            
def student_register(request):
    colleges = College.objects.all()
    if request.method == "POST":

        # --- Get form data ---
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        college_id = request.POST.get("college")
        department_id = request.POST.get("department")
        course_id = request.POST.get("course")

        id_card = request.FILES.get("idphoto")

        # --- Validation ---
        if not all([first_name,last_name, email, phone, password, college_id, department_id, course_id, id_card]):
            messages.error(request, "All fields are required")
            return redirect("student_register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("student_register")

        # --- Save student ---
        user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name =first_name,
                    last_name =last_name,
                    
                )
        user.groups.add(Group.objects.get(name='user'))
        
        AppUser.objects.create(
            auth_user = user,
            phone=phone,
            role='STUDENT',
            college=College.objects.get(id=college_id),
            department=Department.objects.get(id=department_id),
            course=Course.objects.get(id=course_id),
            id_photo=id_card   # ✅ Django saves file automatically
        )

        messages.success(request, "Student registered successfully!")
        return redirect("home")

    # GET request
    return render(request, "authapp/student-registration.html",{'colleges': colleges})

     


    

