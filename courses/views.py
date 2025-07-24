from django.shortcuts import render, redirect, get_object_or_404
from .forms import CourseForm, ModuleForm, LessonForm, QuizForm, QuestionForm, TakeQuizForm, AnnouncementForm, LessonCommentForm, CourseReportForm, LessonFileFormSet
from .models import Course, Module, Lesson, Quiz, Question, QuizAttempt, LessonProgress, Certificate, LessonFile, Announcement
from django.contrib.auth.decorators import login_required
import markdown
from django.utils.safestring import mark_safe
from django.db.models import Q 
from django.db import models
from django.http import HttpResponse, HttpResponseForbidden, FileResponse, Http404, JsonResponse
from django.contrib import messages
from .utils import is_course_completed
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from datetime import datetime
from adminpanel.utils import log_moderation_action
from django.core.paginator import Paginator
import pdfkit

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('dashboard')
    else:
        form = CourseForm()
    return render(request, 'courses/course/create_course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/course/edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not request.user.is_superuser and course.instructor != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        log_moderation_action(request.user, 'delete_course', course)
        course.delete()
        return redirect('admin_dashboard' if request.user.is_superuser else 'dashboard')

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = request.user in course.enrolled_users.all()
    html_description = mark_safe(markdown.markdown(course.description))

    lessons = Lesson.objects.filter(module__course=course, is_approved=True)
    completed_lessons = LessonProgress.objects.filter(user=request.user, lesson__in=lessons, completed=True).count()
    course_completed = completed_lessons == lessons.count()

    if request.method == 'POST':
        if is_enrolled:
            course.enrolled_users.remove(request.user)
        else:
            course.enrolled_users.add(request.user)
        return redirect('course_detail', course_id=course.id)
    elif 'report' in request.POST:
            report_form = CourseReportForm(request.POST)
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.reporter = request.user
                report.course = course
                report.save()
                return redirect('course_detail', course_id=course.id)
    
    comment_form = LessonCommentForm()

    progress_dict = {}
    for module in course.modules.filter(is_approved=True):
        for lesson in module.lessons.filter(is_approved=True):
            progress = lesson.lessonprogress_set.filter(user=request.user).first()
            progress_dict[lesson.id] = progress

    attempt_dict = {}
    for module in course.modules.filter(is_approved=True):
        for lesson in module.lessons.filter(is_approved=True):
            quizzes = lesson.quiz.filter(is_approved=True)
            for quiz in quizzes:
                attempt = quiz.quizattempt_set.filter(user=request.user).first()
                if attempt:
                    attempt_dict[quiz.id] = attempt


    return render(request, 'courses/course/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'html_description': html_description,
        'comment_form': comment_form,
        'progress_dict': progress_dict,
        'attempt_dict': attempt_dict,
        'course_completed': course_completed, 
    })

@login_required
def get_scan_status(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons_data = []
    files_data = []

    for module in course.modules.all():
        for lesson in module.lessons.all():
            lessons_data.append({
                "id": lesson.id,
                "status": lesson.video_scan_status,
            })
            for file in lesson.files.all():
                files_data.append({
                    "id": file.id,
                    "status": file.file_scan_status,
                })

    return JsonResponse({"lessons": lessons_data, "files": files_data})

@login_required
def browse_courses(request):
    query = request.GET.get('q', '')
    date = request.GET.get('date', '')
    page_number = request.GET.get('page', 1)

    courses = Course.objects.exclude(instructor=request.user).filter(is_approved=True)

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(instructor__full_name__icontains=query)
        )

    if date:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            courses = courses.filter(created_at__date=date_obj)
        except ValueError:
            pass

    paginator = Paginator(courses, 9) 
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('courses/course/partials/course_list_partial.html', {
            'courses': page_obj.object_list,
            'page_obj': page_obj,
        })
        return JsonResponse({'html': html})

    return render(request, 'courses/course/browse_courses.html', {
        'courses': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'date': date,
    })

@login_required
def add_module(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect('course_detail', course_id)
    else:
        last_order = course.modules.aggregate(max_order=models.Max('order'))['max_order'] or 0
        form = ModuleForm(initial={'order': last_order + 1})

    return render(request, 'courses/module/add_module.html', {'form': form, 'course': course})

@login_required
def edit_module(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('course_detail', module.course.id)
    else:
        form = ModuleForm(instance=module)
    return render(request, 'courses/module/edit_module.html', {'form': form, 'module': module})


@login_required
def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    if request.method == 'POST':
        course_id = module.course.id
        module.delete()
        return redirect('course_detail', course_id)



@login_required
def add_lesson(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')  
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            for f in files:
                LessonFile.objects.create(lesson=lesson, file=f)
            return redirect('course_detail', course_id=module.course.id)
    else:
        form = LessonForm()

    return render(request, 'courses/lesson/add_lesson.html', {'form': form, 'module': module})

@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)
    module = lesson.module

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        files = request.FILES.getlist('files')
        file_formset = LessonFileFormSet(request.POST, request.FILES, queryset=lesson.files.all(), prefix='files')

        if form.is_valid() and file_formset.is_valid():
            form.save()

            for file_form in file_formset:
                if file_form.cleaned_data.get('DELETE') and file_form.instance.pk:
                    file_form.instance.delete()

            instances = file_formset.save(commit=False)
            for inst in instances:
                inst.lesson = lesson
                inst.save()

            for f in files:
                LessonFile.objects.create(lesson=lesson, file=f)

            return redirect('course_detail', course_id=module.course.id)
    else:
        form = LessonForm(instance=lesson)
        file_formset = LessonFileFormSet(queryset=lesson.files.all(), prefix='files')

    return render(request, 'courses/lesson/edit_lesson.html', {
        'form': form,
        'file_formset': file_formset,
        'lesson': lesson,
        'module': module,
    })

@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)
    course_id = lesson.module.course.id
    if request.method == 'POST':
        lesson.delete()
        return redirect('course_detail', course_id=course_id)


@login_required
def create_quiz(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.lesson = lesson
            quiz.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuizForm()

    return render(request, 'courses/quiz/create_quiz.html', {'form': form, 'lesson': lesson})

@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, lesson__module__course__instructor=request.user)
    lesson = quiz.lesson

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=quiz.lesson.module.course.id)
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'courses/quiz/edit_quiz.html', {'form': form, 'lesson': lesson, 'quiz': quiz})

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, lesson__module__course__instructor=request.user)
    course_id = quiz.lesson.module.course.id 

    if request.method == 'POST':
        quiz.delete()
        return redirect('course_detail', course_id=course_id)



@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, lesson__module__course__instructor=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, "✅ Question added successfully!")
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuestionForm()

    return render(request, 'courses/question/add_question.html', {'form': form, 'quiz': quiz})

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, quiz__lesson__module__course__instructor=request.user)
    quiz = question.quiz

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('view_quiz', quiz_id=quiz.id)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'courses/question/edit_question.html', {'form': form, 'quiz': quiz, 'question': question})


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(
        Question, 
        id=question_id, 
        quiz__lesson__module__course__instructor=request.user
    )
    quiz = question.quiz
    if request.method == 'POST':
        question.delete()
        return redirect('add_question', quiz_id=quiz.id)


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    lesson = quiz.lesson

    if not lesson.module.course.enrolled_users.filter(id=request.user.id).exists():
        return HttpResponseForbidden("You are not enrolled or quiz not available.")

    user_attempts = QuizAttempt.objects.filter(quiz=quiz, user=request.user)
    attempts_used = user_attempts.count()

    if attempts_used >= quiz.max_attempts:
        return render(request, 'courses/quiz/quiz_already_taken.html', {
            'lesson': lesson,
            'attempts': attempts_used,
            'max_attempts': quiz.max_attempts,
        })

    questions = quiz.questions.all()

    if request.method == 'POST':
        form = TakeQuizForm(request.POST, questions=questions)
        if form.is_valid():
            correct = 0
            results = []

            for question in questions:
                user_answer = form.cleaned_data.get(f"question_{question.id}", "").strip()
                correct_answer = question.correct_answer.strip()
                explanation = question.explanation or "No explanation provided."

                is_correct = user_answer.lower() == correct_answer.lower()
                if is_correct:
                    correct += 1

                results.append({
                    'question': question.question_text,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'is_correct': is_correct,
                    'explanation': explanation,
                })

            score = round((correct / len(questions)) * 10, 2)

            QuizAttempt.objects.create(quiz=quiz, user=request.user, score=score)

            request.session['quiz_results'] = {
                'score': score,
                'results': results,
                'quiz_id': quiz.id,
            }

            return redirect('quiz_result', quiz_id=quiz.id)
    else:
        form = TakeQuizForm(questions=questions)

    return render(request, 'courses/quiz/take_quiz.html', {
        'form': form,
        'lesson': lesson,
        'quiz': quiz,
        'time_limit': quiz.time_limit,
        'attempts_used': attempts_used,
        'attempts_left': max(0, quiz.max_attempts - attempts_used),
    })


@login_required
def quiz_result(request, quiz_id):
    data = request.session.pop('quiz_results', None)
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if not data or data['quiz_id'] != quiz.id:
        return redirect('course_detail', quiz.lesson.module.course.id)

    lesson = quiz.lesson
    attempts_used = QuizAttempt.objects.filter(quiz=quiz, user=request.user).count()
    attempts_left = max(0, quiz.max_attempts - attempts_used)

    return render(request, 'courses/quiz/quiz_result.html', {
        'score': data['score'],
        'results': data['results'],
        'lesson': lesson,
        'attempts_used': attempts_used,
        'attempts_left': attempts_left,
    })

@login_required
def view_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    question_forms = []
    for question in questions:
        form = QuestionForm(instance=question)
        question_forms.append((form, question))

    is_instructor = quiz.lesson.module.course.instructor == request.user

    return render(request, 'courses/quiz/view_quiz.html', {
        'quiz': quiz,
        'lesson': quiz.lesson,
        'question_forms': question_forms,
        'is_instructor': is_instructor,
    })

@login_required
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course
    if not course.enrolled_users.filter(id=request.user.id).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")

    LessonProgress.objects.update_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': True}
    )

    return redirect('course_detail', course_id=course.id)

def generate_certificate(request, course_id):

    course = get_object_or_404(Course, pk=course_id)
    context = {
        'course': course,
        'user': request.user,
    }

    html_string = render_to_string('courses/certificate.html', context)
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    pdf = pdfkit.from_string(html_string, False, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    return response

@login_required
def add_announcement(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.instructor:
        return redirect('course_detail', course_id=course.id)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.course = course
            announcement.author = request.user  
            announcement.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = AnnouncementForm()
    
    return render(request, 'courses/announcement/add_announcement.html', {'form': form, 'course': course})

@login_required
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id, author=request.user)
    course = announcement.course

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'courses/announcement/edit_announcement.html', {'form': form, 'course': course, 'announcement': announcement})

@login_required
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id, author=request.user)
    course = announcement.course

    if request.method == 'POST':
        announcement.delete()
        return redirect('course_detail', course_id=course.id)

@login_required
def post_comment(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course

    if not (request.user == course.instructor or course.enrolled_users.filter(id=request.user.id).exists()):
        return HttpResponseForbidden("Not allowed.")

    if request.method == 'POST':
        form = LessonCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.lesson = lesson
            comment.save()
            return redirect('course_detail', course_id=course.id)
    return HttpResponse("Invalid comment", status=400)

@login_required
def download_file(request, file_id):
    try:
        file = get_object_or_404(LessonFile, id=file_id)
        response = FileResponse(file.file.open(), as_attachment=True, filename=file.file.name)
        return response
    except Exception:
        raise Http404("File not found.")
    
@login_required
def report_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = CourseReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.course = course
            report.reporter = request.user
            report.save()
            messages.success(request, '✅ Your report has been submitted successfully.')
            return redirect('course_detail', course_id=course.id)
        else:
            messages.error(request, '❌ Please correct the errors in the form.')
    else:
        form = CourseReportForm()

    return render(request, 'courses/course/report_course.html', {
        'form': form,
        'course': course
    })