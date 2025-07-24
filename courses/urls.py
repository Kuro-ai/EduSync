from django.urls import path
from . import views

urlpatterns = [
    #course management URLs
    path('create/', views.create_course, name='create_course'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('browse/', views.browse_courses, name='browse_courses'),
    
    #module management URLs
    path('course/<int:course_id>/add-module/', views.add_module, name='add_module'),
    path('module/<int:module_id>/edit/', views.edit_module, name='edit_module'),
    path('module/<int:module_id>/delete/', views.delete_module, name='delete_module'),

    #lesson management URLs
    path('module/<int:module_id>/add-lesson/', views.add_lesson, name='add_lesson'),
    path('lesson/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),

    #quiz management URLs
    path('lesson/<int:lesson_id>/create-quiz/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/view/', views.view_quiz, name='view_quiz'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    
    #question management URLs
    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    
    path('lesson/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('certificate/<int:course_id>/', views.generate_certificate, name='generate_certificate'),
    
    #announcement management URLs
    path('course/<int:course_id>/add-announcement/', views.add_announcement, name='add_announcement'),
    path('announcement/<int:announcement_id>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcement/<int:announcement_id>/delete/', views.delete_announcement, name='delete_announcement'),

    path('lessons/<int:lesson_id>/comment/', views.post_comment, name='post_comment'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('course/<int:course_id>/report/', views.report_course, name='report_course'),
    path('courses/<int:course_id>/scan-status/', views.get_scan_status, name='get_scan_status')

]
