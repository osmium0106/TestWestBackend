from django.contrib.auth.models import AbstractUser
from django.db import models
from questions.models import Grade, Subject, Chapter, Topic

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

class UserPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preference')
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    chapters = models.ManyToManyField(Chapter, blank=True)
    topics = models.ManyToManyField(Topic, blank=True)
    subtopics = models.ManyToManyField('questions.Subtopic', blank=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
