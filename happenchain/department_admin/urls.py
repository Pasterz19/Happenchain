from django.urls import path
from . import views

app_name ='department_admin'

urlpatterns = [
    path("", views.overview, name="dashboard-overview"),
    path("events/", views.events, name="dashboard-events"),
    # path("registrations/", views.registrations, name="dashboard-registrations"),
    path("analytics/", views.analytics, name="dashboard-analytics"),
    path("registrations/",views.department_registrations,name="department-registrations"),
    path("student-registrations/",views.student_registration_requests,name="student-registrations"),
    path("student-registrations/<int:student_id>/toggle/",views.toggle_student_status, name="toggle-student-status" ),
     path("events/create/",views.create_event,name="create-event" ),
      path( "sub-events/create/",views.create_sub_event,name="create-sub-event"),
       path("profile/", views.profile, name="profile"),
       path("complaints/", views.my_complaints, name="my_complaints"),
       path("complaints/submit/", views.submit_complaint, name="submit_complaint"),
       path("events/edit/<int:event_id>/", views.edit_event, name="edit-event"),
       path("sub-events/edit/<int:sub_event_id>/", views.edit_sub_event, name="edit-sub-event"),
]
