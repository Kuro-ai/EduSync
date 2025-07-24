from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('verify/<str:token>/', views.verify_email_view, name='verify_email'),
    path('resend-verification/', views.resend_verification_email, name='resend_verification_email'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('faq/', views.faq, name='faq'),
    path('test-verification/', views.send_test_verification_email, name='test_verification'),
     path('profile/', views.profile_view, name='profile'),
    path('', lambda request: redirect('dashboard/')),
]
