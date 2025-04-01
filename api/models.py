from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
from datetime import date, datetime



class userRoles(models.Model):
    ROLE_CHOICES = [
        ('Strategic Affairs', 'Strategic Affairs'),
        ('Minister', 'Minister'),
        ('State', 'State'),
        ('CEO', 'CEO'),
        ('Departments', 'Departments'),
        ('Affiliated', 'Affiliated'),
        ('Supporting', 'Supporting'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roles = models.CharField(max_length=50, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      return self.roles
    


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # is_superuser = None  
    username = models.CharField(max_length=100, unique=True, verbose_name="Office Name")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(
        userRoles, 
        on_delete=models.CASCADE,
        related_name='userroles',
        null=True,
        blank=True
    )
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    
    def __str__(self):
        return self.username
    


class Deadline(models.Model):
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def is_past_deadline(self):
        return timezone.now() > self.deadline

    def __str__(self):
        return self.deadline



class Goal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class KRA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal = models.ForeignKey(Goal, related_name='kras', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class KPI(models.Model):
    UNIT_CHOICES = [
        ('Number', 'Number'),
        ('Percent', 'Percent')
    ]


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kra = models.ForeignKey(KRA, related_name='kpis', on_delete=models.CASCADE)
    unit = models.CharField(max_length=255, choices=UNIT_CHOICES)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Year(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.year)
    

class KPIValue(models.Model):
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='values')
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='kpi_values')
    target = models.FloatField()
    actual = models.FloatField()

    def __str__(self):
        return f"{self.kpi.name} ({self.year.year}): {self.value}"


class Plan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='plan')
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='docs')
    description = models.CharField(max_length=50)
    feedback = models.CharField(max_length=50, default="No feedback")
    submission_date = models.DateField(default=date.today)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    sender = models.ManyToManyField(get_user_model(), null=True, blank=True)
    receivers = models.ManyToManyField(get_user_model(), related_name='submitted_plans', blank=True)  
    target = models.IntegerField()
    quarter_1 = models.IntegerField()
    quarter_2 = models.IntegerField()
    quarter_3 = models.IntegerField()
    quarter_4 = models.IntegerField()


class QuarterlyReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    QUARTER_CHOICES = [
        (1, 'Quarter 1'),
        (2, 'Quarter 2'),
        (3, 'Quarter 3'),
        (4, 'Quarter 4'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kpi = models.ForeignKey('KPI', on_delete=models.CASCADE)
    year = models.ForeignKey('Year', on_delete=models.CASCADE)
    # quarter = models.IntegerField(choices=QUARTER_CHOICES)
    description = models.CharField(max_length=255)
    feedback = models.CharField(max_length=50, default="No feedback")
    submission_date = models.DateField(default=date.today)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sender = models.ManyToManyField(get_user_model(), blank=True, related_name='quarterly_reports_sent')
    receivers = models.ManyToManyField(get_user_model(), blank=True, related_name='quarterly_reports_received')
    # value = models.IntegerField()
    quarter_1 = models.IntegerField()
    quarter_2 = models.IntegerField(default=0)
    quarter_3 = models.IntegerField(default=0)
    quarter_4 = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.kpi} - {self.year} - Q{self.quarter}"

class PlanDocument(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    year = models.OneToOneField(Year, on_delete=models.CASCADE, related_name='yearly_report_docs')
    submission_date = models.DateField(default=date.today)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    sender = models.ManyToManyField(get_user_model(), null=True, blank=True)
    receivers = models.ManyToManyField(get_user_model(), related_name='received_report_docs', blank=True) 


class ReportDocument(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    QUARTER_CHOICES = [
        (1, 'Quarter 1'),
        (2, 'Quarter 2'),
        (3, 'Quarter 3'),
        (4, 'Quarter 4'),
    ]
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='yearly_plan_docs')
    submission_date = models.DateField(default=date.today)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    quarter = models.IntegerField(choices=QUARTER_CHOICES)
    sender = models.ManyToManyField(get_user_model(), null=True, blank=True)
    receivers = models.ManyToManyField(get_user_model(), related_name='received_plan_docs', blank=True)  


class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    office = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='office_budget')
    year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} Budget - {self.description}"


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ManyToManyField(get_user_model(), related_name='notifications')
    message = models.TextField()
    attachment = models.FileField(upload_to='notifications/attachments/', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"Notification for {self.recipient.username} - {'Read' if self.is_read else 'Unread'}"


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=1000)
#     bio = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="user_images", default="default.jpg")
#     verified = models.BooleanField(default=False)


#     def __str__(self):
#         return self.full_name

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)
    



