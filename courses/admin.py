from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Course, Module, Lesson, Announcement, Quiz, Question, LessonComment, CourseReport

admin.site.register(Course, MarkdownxModelAdmin)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(LessonComment)
admin.site.register(CourseReport)
admin.site.register(Announcement)