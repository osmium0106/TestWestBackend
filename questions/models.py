from django.db import models

class Grade(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects')
    def __str__(self):
        return f"{self.grade} - {self.name}"

class Chapter(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    def __str__(self):
        return f"{self.subject} - {self.name}"

class Topic(models.Model):
    name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='topics')
    def __str__(self):
        return f"{self.chapter} - {self.name}"

class Subtopic(models.Model):
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    def __str__(self):
        return f"{self.topic} - {self.name}"

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'MCQ'),
        ('msq', 'MSQ'),
        ('short', 'Short'),
        ('long', 'Long'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    text = models.TextField()
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    extra_field1 = models.CharField(max_length=100, blank=True, null=True)
    extra_field2 = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.text[:50]}..."
