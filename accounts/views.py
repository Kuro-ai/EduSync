from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import CustomUserSignupForm, CustomLoginForm, ProfileUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Avg
from courses.models import Course, LessonProgress, QuizAttempt
from django.utils.timezone import now, timedelta
from django.utils import timezone
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages 

@login_required
def dashboard_view(request):
    user = request.user
    created_courses = Course.objects.filter(instructor=user).prefetch_related('enrolled_users', 'modules__lessons')
    enrolled_courses = user.enrolled_courses.exclude(instructor=user)
    unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    course_data = []
    for course in created_courses:
        students = course.enrolled_users.all()
        lesson_ids = []
        for module in course.modules.all():
            lesson_ids.extend(module.lessons.values_list('id', flat=True))

        student_progress = {}
        for student in students:
            completed_count = LessonProgress.objects.filter(user=student, lesson_id__in=lesson_ids, completed=True).count()
            total_lessons = len(lesson_ids)

            avg_quiz_score = QuizAttempt.objects.filter(user=student, quiz__lesson__module__course=course).aggregate(
                avg_score=Avg('score')
            )['avg_score'] or 0

            student_progress[student] = {
                'completed_lessons': completed_count,
                'total_lessons': total_lessons,
                'avg_quiz_score': round(avg_quiz_score, 2),
            }

        course_data.append({
            'course': course,
            'student_progress': student_progress,
        })

    context = {
        'created_courses': created_courses,
        'enrolled_courses': enrolled_courses,
        'course_data': course_data,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'accounts/dashboard.html', context)


signer = TimestampSigner()
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.verification_sent_at = now()
            user.save()
            
            token = signer.sign(user.pk)
            verification_url = request.build_absolute_uri(
                reverse('verify_email', kwargs={'token': token})
            )

            subject = 'EduSync – Activate Your Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [user.email]

            html_content = render_to_string('emails/verify_email.html', {
                'user': user,
                'verification_url': verification_url
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(subject, text_content, from_email, to)
            email.attach_alternative(html_content, "text/html")
            email.send()

            return render(request, 'emails/email_sent.html')
    else:
        form = CustomUserSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def verify_email_view(request, token):
    try:
        user_id = signer.unsign(token, max_age=600)  
        user = CustomUser.objects.get(pk=user_id)
        user.is_email_verified = True
        user.is_active = True
        user.save()
        login(request, user)

        return render(request, 'emails/verification_success.html', {
            'message': "Your email has been successfully verified!",
            'redirect_url': reverse('dashboard')
        })

    except (BadSignature, SignatureExpired, CustomUser.DoesNotExist):
        return render(request, 'emails/verification_failed.html', {
            'message': 'Verification link is invalid or has expired. Please sign up again.'
        })

@login_required
def resend_verification_email(request):
    user = request.user
    if user.is_email_verified:
        return redirect('dashboard')

    signer = TimestampSigner()
    token = signer.sign(user.email)
    verification_url = request.build_absolute_uri(
        reverse('verify_email') + f'?token={token}'
    )
    subject = 'Resend: Verify your email'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    html_content = render_to_string('emails/reverify_email.html', {
        'user': user,
        'verification_url': verification_url
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    user.verification_sent_at = timezone.now()
    user.save()
    return render(request, 'emails/email_sent.html')

@login_required
def send_test_verification_email(request):
    user = request.user
    token = signer.sign(user.pk)
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'token': token})
    )

    subject = 'Test Email – EduSync Verification'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    html_content = render_to_string('emails/verify_email.html', {
        'user': user,
        'verification_url': verification_url
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()

    return HttpResponse("Test email sent.")

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if user.is_timed_out():
                remaining = user.timeout_until - now()
                hours, remainder = divmod(remaining.total_seconds(), 3600)
                minutes = remainder // 60
                form.add_error(
                    None,
                    f"Your account is temporarily suspended. Time remaining: {int(hours)}h {int(minutes)}m."
                )
                return render(request, 'accounts/login.html', {'form': form})

         
            if not user.is_email_verified:

                token = signer.sign(user.pk)
                verification_url = request.build_absolute_uri(
                    reverse('verify_email', kwargs={'token': token})
                )

                send_mail(
                    'Verify your email',
                    f'Click the link to verify: {verification_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )

                return render(request, 'emails/email_sent.html', {
                    'message': 'Your email is not verified. A new verification link has been sent to your email.'
                })

            login(request, user)
            return redirect('admin_dashboard' if user.is_staff else 'dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def privacy_policy(request):
    return render(request, 'privacy.html')

def terms_of_service(request):
    return render(request, 'terms.html')

def faq(request):
    return render(request, 'faq.html')

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user, request.POST)
            profile_form = ProfileUpdateForm(instance=user)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                # Send confirmation email
                subject = 'Your EduSync Password Has Been Changed'
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [user.email]
                html_content = render_to_string('accounts/password_change_confirmation.html', {'user': user})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(subject, text_content, from_email, to)
                email.attach_alternative(html_content, "text/html")
                email.send()

                messages.success(request, "✅ Your password has been changed successfully.")
                return redirect('profile')

        elif 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            password_form = CustomPasswordChangeForm(user)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "✅ Your profile has been updated.")
                return redirect('profile')

    else:
        profile_form = ProfileUpdateForm(instance=user)
        password_form = CustomPasswordChangeForm(user)

    return render(request, 'accounts/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })