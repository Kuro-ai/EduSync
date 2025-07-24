from django.core.management.base import BaseCommand
from courses.models import Lesson, LessonFile
from courses.utils import scan_url_with_virustotal, scan_file_with_virustotal

class Command(BaseCommand):
    help = "Check pending VirusTotal scans and update their statuses."

    def handle(self, *args, **kwargs):
        pending_lessons = Lesson.objects.filter(video_scan_status='pending')
        for lesson in pending_lessons:
            new_status = scan_url_with_virustotal(lesson.video_url)
            if new_status != "pending":
                lesson.video_scan_status = new_status
                lesson.save(update_fields=['video_scan_status'])
                self.stdout.write(f"Updated Lesson {lesson.id} video_scan_status to {new_status}")

        pending_files = LessonFile.objects.filter(file_scan_status='pending')
        for file in pending_files:
            new_status = scan_file_with_virustotal(file.file.path)
            if new_status != "pending":
                file.file_scan_status = new_status
                file.save(update_fields=['file_scan_status'])
                self.stdout.write(f"Updated File {file.id} file_scan_status to {new_status}")
