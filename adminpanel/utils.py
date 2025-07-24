from .models import ModerationLog

def log_moderation_action(admin_user, action, target_instance):
    ModerationLog.objects.create(
        admin=admin_user,
        action=action,
        target_type=target_instance.__class__.__name__,
        target_id=target_instance.id,
        target_repr=str(target_instance),
    )
