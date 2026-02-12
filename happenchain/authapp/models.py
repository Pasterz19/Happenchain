from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class College(models.Model):
    VERIFICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    declaration_document = models.FileField(
        upload_to='college_declarations/',
        null=True,
        blank=True
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default='PENDING'
    )

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Degree(models.Model):
    LEVEL_CHOICES = [
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('PHD', 'Doctoral'),
        ('DIP', 'Diploma'),
        ('CERT', 'Certificate'),
    ]

    name = models.CharField(max_length=50)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.level})"

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration_years = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class EventType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    venue = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    event_photo = models.FileField(
        upload_to='event_photo/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

class SubEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    cost = models.DecimalField( max_digits=8,decimal_places=2,null=True,blank=True)
    is_team_event = models.BooleanField(default=False)
    min_team_size = models.PositiveIntegerField(null=True, blank=True)
    max_team_size = models.PositiveIntegerField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Team(models.Model):
    sub_event = models.ForeignKey(SubEvent, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('LEADER', 'Leader'),
        ('MEMBER', 'Member'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Registration(models.Model):
    sub_event = models.ForeignKey(SubEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registration - {self.sub_event.title}"

class Payment(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100)
    paid_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class AppUser(models.Model):
    ROLE_CHOICES = [
        ('COLLEGE_ADMIN', 'College Admin'),
        ('DEPT_ADMIN', 'Department Admin'),
        ('STUDENT', 'Student'),
    ]
    VERIFICATION_STATUS = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=11)
    college = models.ForeignKey(College, null=True, blank=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    
    id_photo = models.FileField(
        upload_to='user_id_photos/',
        null=True,
        blank=True
    )
    profile_pic = models.FileField(
        upload_to='user_profile_pics/',
        null=True,
        blank=True
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default='PENDING'
    )

class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]

    from_user = models.ForeignKey(
        User,
        related_name="sent_friend_requests",
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name="received_friend_requests",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.status})"

