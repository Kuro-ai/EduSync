from .models import Notification

def notify_user(user, message):
    Notification.objects.create(recipient=user, message=message)