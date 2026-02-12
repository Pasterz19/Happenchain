from django.urls import path
from . import views

app_name = "appuser"

urlpatterns = [
    path('', views.user_dashboard, name="user_dashboard"),
    path("profile/", views.user_profile, name="user_profile"),
    path( "events/<event_id>/sub-events/",views.fetch_sub_events,name="fetch_sub_events"),
    path("register-sub-event/",views.register_sub_event,name="register_sub_event"),
    path("friends/", views.friends_list, name="friends"),
    path("friends/requests/", views.friend_requests, name="friend_requests"),
    path("friends/accept/<int:request_id>/", views.accept_friend, name="accept_friend"),
    path("friends/reject/<int:request_id>/", views.reject_friend, name="reject_friend"),
    path("register/details/", views.registration_details, name="registration_details"),
    path("payment/preview/", views.payment_preview, name="payment_preview"),
    # path("payment/confirm/", views.confirm_payment, name="confirm_payment"),
     path("registrations/", views.my_registrations, name="registrations"),
    path("payments/", views.my_payments, name="payments"),
    path("complaints/", views.my_complaints, name="my_complaints"),
    path("complaints/submit/", views.submit_complaint, name="submit_complaint"),
]
