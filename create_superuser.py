import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
full_name = os.environ.get("DJANGO_SUPERUSER_FULL_NAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(email=email).exists():
    print(f"Creating superuser with email: {email}")
    User.objects.create_superuser(
        email=email,
        password=password,
        full_name=full_name,
        is_staff=True,
        is_superuser=True,
    )
else:
    print(f"Superuser with email {email} already exists")
