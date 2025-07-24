from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class ModerationLog(models.Model):
    ACTION_CHOICES = [
        ('approve', 'Approved'),
        ('revoke', 'Revoked'),
        ('suspend', 'User Suspended'),
        ('unsuspend', 'User Unsuspended'),
        ('delete_course', 'Deleted Course'),
        ('promote_to_staff', 'Promotion'),
        ('demote_from_staff', 'Demotion'),
    ]


    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='moderation_logs'
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    target_type = models.CharField(max_length=50)  
    target_id = models.IntegerField()
    target_repr = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin} - {self.action} - {self.target_type}({self.target_id})"

