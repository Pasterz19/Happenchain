from django.urls import path
from . import views

app_name='college_admin'

urlpatterns = [
    path('', views.college_admin_dashboard, name='dashboard'),
    path('events/', views.events_registry, name='events_registry'),
    path('analytics/', views.analytics, name='analytics'),
    path('settings/', views.settings, name='settings'),
    path("department-admins/",views.department_admins,name="department_admins"),
    path("department-admins/toggle/<int:user_id>/",views.toggle_department_admin,name="toggle_department_admin"),
    path("events/",views.events_registry,name="events_registry"),
    path("profile/",views.college_admin_profile,name="college_admin_profile"),
    path("complaints/", views.my_complaints, name="my_complaints"),
    path("complaints/submit/", views.submit_complaint, name="submit_complaint"),

    # Course Management
    path("courses/", views.manage_courses, name="manage_courses"),
    path("courses/add/", views.add_course, name="add_course"),
    path("courses/edit/<int:course_id>/", views.edit_course, name="edit_course"),
    path("courses/delete/<int:course_id>/", views.delete_course, name="delete_course"),

    # Department Management
    path("departments/", views.manage_departments, name="manage_departments"),
    path("departments/add/", views.add_department, name="add_department"),
    path("departments/edit/<int:dept_id>/", views.edit_department, name="edit_department"),
    path("departments/delete/<int:dept_id>/", views.delete_department, name="delete_department"),
]
