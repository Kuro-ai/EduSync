from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.utils.timezone import now
from datetime import timedelta

@login_required
def notification_list(request):

    thirty_days_ago = now() - timedelta(days=30)
    Notification.objects.filter(recipient=request.user, created_at__lt=thirty_days_ago).delete()

    limit = int(request.GET.get('limit', 5))
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:limit]
    total_count = Notification.objects.filter(recipient=request.user).count()

    context = {
        'notifications': notifications,
        'has_more': limit < total_count,
        'next_limit': limit + 5,
    }
    return render(request, 'notifications.html', context)


@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    if request.method == 'POST':
        notification.is_read = True
        notification.save()
    return redirect('notification_list')

@login_required
def mark_all_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notification_list')
