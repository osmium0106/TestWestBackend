from django.db import models
from django.contrib.auth import get_user_model
from questions.models import Question

User = get_user_model()

# Create your models here.

class GeneratedPaper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='papers')
    created_at = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField(Question)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Paper for {self.user.username} at {self.created_at}"
