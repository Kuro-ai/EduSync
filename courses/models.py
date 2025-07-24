from django.db import models
from django.conf import settings
from markdownx.models import MarkdownxField
from django.contrib.auth import get_user_model

User = get_user_model()
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = MarkdownxField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    enrolled_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_courses',
        blank=True
    )
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.course.title})"

class Lesson(models.Model):
    SCAN_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("clean", "Clean"),
        ("malicious", "Malicious"),
        ("error", "Error"),
    ]

    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = MarkdownxField(blank=True)
    video_url = models.URLField(blank=True)
    video_scan_status = models.CharField(max_length=10, choices=SCAN_STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class LessonFile(models.Model):
    SCAN_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("clean", "Clean"),
        ("unsafe", "Unsafe"),
        ("error", "Error"),
    ]

    lesson = models.ForeignKey('Lesson', related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='lesson_files/')
    file_scan_status = models.CharField(max_length=10, choices=SCAN_STATUS_CHOICES, default="pending")

    def __str__(self):
        return self.file.name

class Quiz(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes", default=0) 
    max_attempts = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return f"Quiz: {self.title}"

class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('FB', 'Fill in the Blank'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    correct_answer = models.CharField(max_length=255, blank=True, null=True)  # For MCQ & TF
    choices = models.TextField(blank=True, help_text="Comma-separated options for MCQ only")
    explanation = models.TextField(blank=True, help_text="Explain the correct answer (optional)")
    is_approved = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.quiz.title} - {self.question_text[:50]}"

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.score}"

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.email} - {self.lesson.title}"

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"Certificate - {self.user.email} - {self.course.title}"
    
class Announcement(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class LessonComment(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.lesson.title}"    
    
class CourseReport(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reporter.email} on {self.course.title}"
    
class VirusTotalScan(models.Model):
    resource = models.CharField(max_length=500, unique=True) 
    scan_date = models.DateTimeField(auto_now=True)
    scan_result = models.JSONField()  
    is_clean = models.BooleanField(default=False)

    def __str__(self):
        return f"VT Scan: {self.resource} - Clean: {self.is_clean}"