from django.shortcuts import redirect, render,get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.utils.crypto import get_random_string
from authapp.models import Event, FriendRequest, Payment, SubEvent, Registration, Team, TeamMember

# Create your views here.
@never_cache
@login_required
def user_dashboard(request):
    events = Event.objects.select_related(
        "department", "event_type"
    ).prefetch_related("subevent_set")

    friends = get_friends(request.user)

    return render(request, "appuser/dashboard.html", {
        "events": events,
        "friends":friends,
    })

@never_cache
@login_required
def user_profile(request):
    if request.method == "POST":
        user = request.user
        app_user = user.appuser

        # Update User model fields
        full_name = request.POST.get("first_name", "").strip()
        if full_name:
            if " " in full_name:
                user.first_name, *last = full_name.split()
                user.last_name = " ".join(last)
            else:
                user.first_name = full_name
                user.last_name = ""
        
        new_email = request.POST.get("email")
        if new_email and new_email != user.email:
            if User.objects.filter(username=new_email).exists():
                messages.error(request, "This email is already in use.")
                return redirect("appuser:user_profile")
            user.email = new_email
            user.username = new_email  # Sync username with email
        
        user.save()

        # Update AppUser model fields
        app_user.phone = request.POST.get("phone")
        
        if "profile_pic" in request.FILES:
            app_user.profile_pic = request.FILES["profile_pic"]
            
        app_user.save()
        
        messages.success(request, "Profile updated successfully")
        return redirect("appuser:user_profile")

    return render(request, "appuser/profile.html")

@never_cache
@login_required
def fetch_sub_events(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    sub_events = event.subevent_set.all().values(
        "id",
        "title",
        "description",
        "is_team_event",
        "min_team_size",
        "max_team_size",
        "cost"
    )

    return JsonResponse({
        "event": event.title,
        "sub_events": list(sub_events)
    })

@never_cache
@login_required
def register_sub_event(request):
    if request.method != "POST":
        return redirect("user_dashboard")

    sub_event = get_object_or_404(
        SubEvent, id=request.POST.get("sub_event_id")
    )

    # =========================
    # TEAM EVENT
    # =========================
    if sub_event.is_team_event:
        team_name = request.POST.get("team_name")
        member_ids = request.POST.getlist("team_members")  # friend IDs

        if not team_name:
            messages.error(request, "Team name is required")
            return redirect("user_dashboard")

        # Friends validation
        friends = get_friends(request.user)
        friend_ids = {f.id for f in friends}

        for uid in member_ids:
            if int(uid) not in friend_ids:
                messages.error(request, "Invalid team member selected")
                return redirect("user_dashboard")

        team_size = 1 + len(member_ids)  # leader + members

        if sub_event.max_team_size and team_size > sub_event.max_team_size:
            messages.error(request, "Team size exceeds limit")
            return redirect("user_dashboard")

        # Create team
        team = Team.objects.create(
            sub_event=sub_event,
            name=team_name,
            created_by=request.user
        )

        # Leader
        TeamMember.objects.create(
            team=team,
            user=request.user,
            role="LEADER"
        )

        # Members
        for uid in member_ids:
            TeamMember.objects.create(
                team=team,
                user_id=uid,
                role="MEMBER"
            )

        Registration.objects.create(
            sub_event=sub_event,
            team=team
        )

    # =========================
    # INDIVIDUAL EVENT
    # =========================
    else:
        Registration.objects.create(
            sub_event=sub_event,
            user=request.user
        )

    messages.success(request, "Successfully registered!")
    return redirect("user_dashboard")

from django.db.models import Q


def get_friends(user):
    requests = FriendRequest.objects.filter(
        Q(from_user=user) | Q(to_user=user),
        status="ACCEPTED"
    )

    friends = []
    for req in requests:
        friends.append(req.to_user if req.from_user == user else req.from_user)

    return friends

@never_cache
@login_required
def friends_list(request):
    # Get friends
    accepted = FriendRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
        status="ACCEPTED"
    )

    friends = [
        fr.to_user if fr.from_user == request.user else fr.from_user
        for fr in accepted
    ]

    # Send request
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            to_user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect("appuser:friends")

        if to_user == request.user:
            messages.error(request, "You cannot add yourself")
            return redirect("appuser:friends")

        FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=to_user
        )

        messages.success(request, "Friend request sent")
        return redirect("appuser:friends")

    return render(request, "appuser/friends/friends_list.html", {
        "friends": friends
    })

@never_cache
@login_required
def friend_requests(request):
    incoming = FriendRequest.objects.filter(
        to_user=request.user,
        status="PENDING"
    )

    outgoing = FriendRequest.objects.filter(
        from_user=request.user,
        status="PENDING"
    )

    return render(request, "appuser/friends/friend_requests.html", {
        "incoming": incoming,
        "outgoing": outgoing
    })

@never_cache
@login_required
def accept_friend(request, request_id):
    fr = get_object_or_404(
        FriendRequest,
        id=request_id,
        to_user=request.user
    )

    fr.status = "ACCEPTED"
    fr.save()

    messages.success(request, "Friend request accepted")
    return redirect("appuser:friend_requests")

@never_cache
@login_required
def reject_friend(request, request_id):
    fr = get_object_or_404(
        FriendRequest,
        id=request_id,
        to_user=request.user
    )

    fr.status = "REJECTED"
    fr.save()

    messages.info(request, "Friend request rejected")
    return redirect("appuser:friend_requests")

@never_cache
@login_required
def registration_details(request):
    sub_event = get_object_or_404(
        SubEvent,
        id=request.GET.get("sub_event_id")
    )

    # Team data from GET
    team_name = request.GET.get("team_name")
    member_ids = request.GET.getlist("team_members")  

    # Fetch selected friends (User objects)
    selected_friends = User.objects.filter(id__in=member_ids)

    amount = sub_event.cost

    return render(request, "appuser/registration_details.html", {
        "sub_event": sub_event,
        "team_name": team_name,
        "selected_friends": selected_friends,
        "amount": amount,
    })

@never_cache
@login_required
@transaction.atomic  # <--- Critical: Ensures data integrity
def payment_preview(request):
    """
    Handles Validation, Registration Creation, Team Creation, 
    and Payment Creation in one single step.
    """
    if request.method != "POST":
        return redirect("appuser:dashboard")

    sub_event_id = request.POST.get("sub_event_id")
    sub_event = get_object_or_404(SubEvent, id=sub_event_id)
    user = request.user

    # ======================================
    # 1. VALIDATION CHECKS
    # ======================================
    
    # Check if already registered (Individual or Team)
    if Registration.objects.filter(sub_event=sub_event, user=user).exists():
        messages.error(request, "You have already registered for this event.")
        return redirect("appuser:dashboard")

    if TeamMember.objects.filter(user=user, team__sub_event=sub_event).exists():
        messages.error(request, "You are already part of a team for this event.")
        return redirect("appuser:dashboard")

    # Initialize variables for creation
    registration = None
    
    # ======================================
    # 2. CREATE REGISTRATION (Team or Individual)
    # ======================================
    try:
        if sub_event.is_team_event:
            team_name = request.POST.get("team_name")
            member_ids = request.POST.getlist("team_members")
            
            # Validate Team Size
            team_size = 1 + len(member_ids) # Leader + Members
            
            if sub_event.min_team_size and team_size < sub_event.min_team_size:
                messages.error(request, f"Minimum team size is {sub_event.min_team_size}")
                return redirect("appuser:dashboard")
            
            if sub_event.max_team_size and team_size > sub_event.max_team_size:
                messages.error(request, f"Maximum team size is {sub_event.max_team_size}")
                return redirect("appuser:dashboard")

            # Create Team
            team = Team.objects.create(
                sub_event=sub_event,
                name=team_name,
                created_by=user
            )

            # Add Leader
            TeamMember.objects.create(team=team, user=user, role="LEADER")

            # Add Members
            for uid in member_ids:
                # Optional: Check if friend is already in another team here
                TeamMember.objects.create(team=team, user_id=uid, role="MEMBER")

            # Create Registration linked to Team
            registration = Registration.objects.create(
                sub_event=sub_event,
                team=team
            )

        else:
            # Individual Registration
            registration = Registration.objects.create(
                sub_event=sub_event,
                user=user
            )

        # ======================================
        # 3. CREATE PAYMENT
        # ======================================
        # ======================================
        # 3. CREATE PAYMENT
        # ======================================
        payment = Payment.objects.create(
            registration=registration,
            amount=sub_event.cost,
            payment_status="SUCCESS",  # Assuming immediate success for now
            transaction_id=get_random_string(12)
        )

        # ======================================
        # 4. SEND EMAIL CONFIRMATION
        # ======================================
        from django.core.mail import send_mail
        from django.conf import settings

        subject = f"Registration Confirmed: {sub_event.title}"
        
        # Prepare content
        reg_type = "Team" if sub_event.is_team_event else "Individual"
        txn_id = payment.transaction_id
        event_date = sub_event.start_time.strftime("%d %b %Y, %I:%M %p")
        
        message = f"""
        Dear {user.first_name},

        Thank you for registering for {sub_event.title}!

        --- Registration Details ---
        Event: {sub_event.event.title}
        Category: {sub_event.title}
        Type: {reg_type}
        Date: {event_date}
        Venue: {sub_event.venue}
        Paid Amount: ₹{sub_event.cost}
        Transaction ID: {txn_id}

        We look forward to seeing you there!

        Best Regards,
        HappenChain Team
        """
        
        # Send email (fail_silently=True to avoid breaking the transaction if mail server is down)
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
        except Exception as mail_error:
            # Log error but don't fail registration
            print(f"Mail sending failed: {mail_error}")

        messages.success(request, f"Successfully registered for {sub_event.title}!")
        return redirect("appuser:registrations") # Redirect to 'My Registrations' page

    except Exception as e:
        # If anything fails inside this block, transaction.atomic 
        # rolls back all DB changes (no zombie teams or unpaid regs).
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("appuser:dashboard")
@never_cache
@login_required
def my_registrations(request):
    registrations = request.user.registration_set.select_related(
        "sub_event",
        "sub_event__event",
        "team"
    ).order_by("-registered_at")

    return render(
        request,
        "appuser/my_registrations.html",
        {"registrations": registrations}
    )

@never_cache
@login_required
def my_payments(request):
    registrations = request.user.registration_set.select_related(
        "payment",
        "sub_event"
    ).filter(payment__isnull=False)

    return render(
        request,
        "appuser/my_payments.html",
        {"registrations": registrations}
    )

from appadmin.models import Complaint

@never_cache
@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "appuser/complaints.html", {"complaints": complaints})

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
        return redirect("appuser:my_complaints")
    return redirect("appuser:my_complaints")
