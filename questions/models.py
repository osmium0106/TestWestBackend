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
    FOUNDATION = 'foundation'
    ADVANCED = 'advanced'
    TAG_CHOICES = [
        (FOUNDATION, 'Foundation'),
        (ADVANCED, 'Advanced'),
    ]
    name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='topics')
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default=FOUNDATION)
    def __str__(self):
        return f"{self.chapter} - {self.name} ({self.get_tag_display()})"

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
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=255, blank=True, null=True, help_text="For MCQ: single letter (a/b/c/d). For MSQ: comma-separated letters (a,b,c)")
    explanation = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.text[:50]}..."
