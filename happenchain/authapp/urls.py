"""
URL configuration for happenchain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
   path('',views.get_home,name='home'),
   path('ajax/load-departments/', views.load_departments, name='ajax_load_departments'),
   path('ajax/load-degrees/', views.load_degrees, name='ajax_load_degrees'),
   path('ajax/load-courses/', views.load_courses, name='ajax_load_courses'),
   #    path('get_student_register_form/',views.get_student_register,name='student_register'),
   path('get_college_register_form/',views.get_college_register,name='college_register'),
   path('post_login/',views.post_login,name='login'),
   path('register_college/',views.college_register,name='post_register_college'),
   path("student/register/", views.student_register, name="student_register"),
   path("logout/", views.common_logout, name="common-logout"),

   # Password Reset URLs
   path('password_reset/', auth_views.PasswordResetView.as_view(
       template_name='authapp/password_reset/password_reset_form.html'
   ), name='password_reset'),
   
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
       template_name='authapp/password_reset/password_reset_done.html'
   ), name='password_reset_done'),
   
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
       template_name='authapp/password_reset/password_reset_confirm.html'
   ), name='password_reset_confirm'),
   
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
       template_name='authapp/password_reset/password_reset_complete.html'
   ), name='password_reset_complete'),
]
