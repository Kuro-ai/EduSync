from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('reports/', views.report_list, name='report_list'),
    path('toggle-course/<int:course_id>/', views.toggle_course_approval, name='toggle_course_approval'),
    path('toggle_timeout/<int:user_id>/', views.admin_toggle_timeout, name='admin_toggle_timeout'),
    path('moderation-logs/', views.moderation_log_view, name='moderation_log'),
    path('toggle-staff/<int:user_id>/', views.toggle_staff_status, name='toggle_staff_status'),
    path('users/', views.admin_users, name='admin_users'),
    path('approvals/', views.admin_approvals, name='admin_approvals'),

]
