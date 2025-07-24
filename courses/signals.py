from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lesson, LessonFile, CourseReport, Module, Quiz
from .utils import scan_url_with_virustotal, scan_file_with_virustotal
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Lesson)
def scan_lesson_video(sender, instance, created, **kwargs):
    if instance.video_url:
        status = scan_url_with_virustotal(instance.video_url)
        if status != instance.video_scan_status:
            instance.video_scan_status = status
            instance.save(update_fields=['video_scan_status'])

@receiver(post_save, sender=LessonFile)
def scan_lesson_file(sender, instance, created, **kwargs):
    if instance.file:
        status = scan_file_with_virustotal(instance.file.path)
        if status != instance.file_scan_status:
            instance.file_scan_status = status
            instance.save(update_fields=['file_scan_status'])

@receiver(post_save, sender=CourseReport)
def notify_admins_on_report(sender, instance, created, **kwargs):
    if created:
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                message=f"A new report has been submitted for course: {instance.course.title}"
            )

@receiver(post_save, sender=Module)
def notify_enrolled_on_module(sender, instance, created, **kwargs):
    if created:
        for user in instance.course.enrolled_users.all():
            Notification.objects.create(
                recipient=user,
                message=f"A new module \"{instance.title}\" was added to your course \"{instance.course.title}\""
            )

@receiver(post_save, sender=Lesson)
def notify_enrolled_on_lesson(sender, instance, created, **kwargs):
    if created:
        course = instance.module.course
        for user in course.enrolled_users.all():
            Notification.objects.create(
                recipient=user,
                message=f"A new lesson \"{instance.title}\" was added to \"{course.title}\""
            )

@receiver(post_save, sender=Quiz)
def notify_enrolled_on_quiz(sender, instance, created, **kwargs):
    if created:
        course = instance.lesson.module.course
        for user in course.enrolled_users.all():
            Notification.objects.create(
                recipient=user,
                message=f"A new quiz \"{instance.title}\" was added to \"{course.title}\""
            )
