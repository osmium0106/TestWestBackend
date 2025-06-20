from django.contrib.auth.models import AbstractUser
from django.db import models
from questions.models import Grade, Subject, Chapter, Topic

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('school_admin', 'School Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_users')
    max_sub_users = models.PositiveIntegerField(default=0, help_text='Max users this admin can create (school_admin only)')
    max_question_papers = models.PositiveIntegerField(default=10, help_text='Max question papers this user can generate')
    school_name = models.CharField(max_length=255, blank=True, null=True, help_text='School name (school_admin only)')
    school_address = models.TextField(blank=True, null=True, help_text='School address (school_admin only)')
    school_contact_number = models.CharField(max_length=50, blank=True, null=True, help_text='School contact number (school_admin only)')
    school_director_name = models.CharField(max_length=255, blank=True, null=True, help_text='School director name (for billing, school_admin only)')
    school_billing_email = models.EmailField(blank=True, null=True, help_text='Billing email (school_admin only)')
    max_question_school_can_generate = models.PositiveIntegerField(default=0, help_text='Max question papers this school can generate (school_admin only)')

class UserPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preference')
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    chapters = models.ManyToManyField(Chapter, blank=True)
    topics = models.ManyToManyField(Topic, blank=True)
    subtopics = models.ManyToManyField('questions.Subtopic', blank=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
