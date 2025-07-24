from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course, Lesson, Quiz, Question, CourseReport
from accounts.models import CustomUser  
from adminpanel.models import ModerationLog
from django.utils.timezone import now, timedelta
from datetime import datetime
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from adminpanel.utils import log_moderation_action
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme

def is_admin(user):
    return user.is_staff or user.is_superuser    

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    email_query = request.GET.get('email', '')
    username_query = request.GET.get('username', '')
    timeout_status = request.GET.get('timeout_status', '')

    users = CustomUser.objects.all()

    if email_query:
        users = users.filter(email__icontains=email_query)

    if username_query:
        users = users.filter(full_name__icontains=username_query.replace('YKPT-', ''))

    if timeout_status == 'timed_out':
        users = users.filter(timeout_until__gt=now())
    elif timeout_status == 'active':
        users = users.filter(Q(timeout_until__isnull=True) | Q(timeout_until__lte=now()))

    context = {
        'users': users,
        'email_query': email_query,
        'username_query': username_query,
        'timeout_status': timeout_status,
        'courses': Course.objects.all(),
        'lessons': Lesson.objects.all(),
        'quizzes': Quiz.objects.all(),
        'questions': Question.objects.all(),
        'now': now(),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('adminpanel/partials/user_list.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'adminpanel/dashboard.html', context)

@require_POST
@user_passes_test(is_admin)
def admin_toggle_timeout(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    action = request.POST.get("action")

    if action == "unsuspend":
        user.timeout_until = None
        log_moderation_action(request.user, 'unsuspend', user)
    elif action == "suspend":
        try:
            hours = int(request.POST.get("hours", 0))
            if hours > 0:
                user.timeout_until = now() + timedelta(hours=hours)
                log_moderation_action(request.user, 'suspend', user)
        except ValueError:
            pass
    user.save()
    return redirect('admin_users')

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def toggle_staff_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.user == user:
        return HttpResponse("You cannot change your own admin status.", status=403)

    if user.is_superuser and user.is_staff:
        return HttpResponse("You cannot demote a superuser from admin.", status=403)

    user.is_staff = not user.is_staff
    user.save()
    action = 'promote_to_staff' if user.is_staff else 'demote_from_staff'
    log_moderation_action(request.user, action, user)

    return redirect('admin_users')

@login_required
@user_passes_test(is_admin)
def report_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    date = request.GET.get('date', '')
    page_number = request.GET.get('page')

    reports = CourseReport.objects.select_related('reporter', 'course')

    if query:
        reports = reports.filter(
            Q(reporter__email__icontains=query) |
            Q(course__title__icontains=query)
        )

    if status == 'approved':
        reports = reports.filter(course__is_approved=True)
    elif status == 'revoked':
        reports = reports.filter(course__is_approved=False)

    if date:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            reports = reports.filter(created_at__date=date_obj)
        except ValueError:
            pass

    reports = reports.order_by('-created_at')
    paginator = Paginator(reports, 10)
    reports_page = paginator.get_page(page_number)

    context = {
        'reports': reports_page,
        'query': query,
        'status': status,
        'date': date,
        'page_obj': reports_page, 
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('adminpanel/partials/report_table.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'adminpanel/report_list.html', context)

@require_POST
@user_passes_test(is_admin)
def toggle_course_approval(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.is_approved = not course.is_approved
    course.save()

    action = 'approve' if course.is_approved else 'revoke'
    log_moderation_action(request.user, action, course)


    subject = f"Your course has been {action}d"
    message = f"Hello {course.instructor.full_name},\n\n" \
              f"Your course \"{course.title}\" has been {action}d by the moderation team.\n\n" \
              f"Best regards,\nEduSync Team"

    recipient_email = course.instructor.email

    html_content = render_to_string("emails/course_status_email.html", {
        "user": course.instructor,
        "course": course,
        "status": "approved" if course.is_approved else "revoked",
    })

    email = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
    email.attach_alternative(html_content, "text/html")
    email.send()

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)

    return redirect('report_list')  

    
@login_required
@user_passes_test(is_admin)
def moderation_log_view(request):
    query = request.GET.get('query', '')
    action_filter = request.GET.get('action', '')
    target_type_filter = request.GET.get('target_type', '')
    date_filter = request.GET.get('date', '')
    page_number = request.GET.get('page', 1)

    logs = ModerationLog.objects.select_related('admin').order_by('-timestamp')

    if query:
        logs = logs.filter(
            Q(admin__email__icontains=query) |
            Q(target_repr__icontains=query)
        )

    if action_filter:
        logs = logs.filter(action=action_filter)

    if target_type_filter:
        logs = logs.filter(target_type__iexact=target_type_filter)

    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            logs = logs.filter(timestamp__date=date_obj)
        except ValueError:
            pass

    paginator = Paginator(logs, 10)  
    page_obj = paginator.get_page(page_number)

    context = {
        'logs': page_obj,
        'page_obj': page_obj,
        'actions': ModerationLog.ACTION_CHOICES,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('adminpanel/partials/moderation_logs_table.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'adminpanel/moderation_logs.html', context)
    
@login_required
@user_passes_test(is_admin)
def admin_users(request):
    email_query = request.GET.get('email', '')
    username_query = request.GET.get('username', '')
    timeout_status = request.GET.get('timeout_status', '')
    page_number = request.GET.get('page')

    users = CustomUser.objects.all()

    if email_query:
        users = users.filter(email__icontains=email_query)

    if username_query:
        users = users.filter(full_name__icontains=username_query.replace('YKPT-', ''))

    if timeout_status == 'timed_out':
        users = users.filter(timeout_until__gt=now())
    elif timeout_status == 'active':
        users = users.filter(Q(timeout_until__isnull=True) | Q(timeout_until__lte=now()))

    users = users.order_by('-date_joined')
    paginator = Paginator(users, 10)  
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'page_obj': page_obj,
        'email_query': email_query,
        'username_query': username_query,
        'timeout_status': timeout_status,
        'now': now(),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('adminpanel/partials/user_list.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'adminpanel/users.html', context)

@login_required
@user_passes_test(is_admin)
def admin_approvals(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    page_number = request.GET.get('page')

    courses = Course.objects.all()

    if search_query:
        courses = courses.filter(title__icontains=search_query)

    if status_filter == 'approved':
        courses = courses.filter(is_approved=True)
    elif status_filter == 'not_approved':
        courses = courses.filter(is_approved=False)

    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            courses = courses.filter(created_at__date=date_obj)
        except ValueError:
            pass

    courses = [c for c in courses if not c.is_approved or c.modules.exists()]

    paginator = Paginator(courses, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        "courses": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "status_filter": status_filter,
        "date_filter": date_filter,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("adminpanel/partials/course_list.html", context, request=request)
        return HttpResponse(html)

    return render(request, "adminpanel/approvals.html", context)