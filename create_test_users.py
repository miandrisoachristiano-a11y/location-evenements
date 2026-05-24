import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from clients.models import Client

# Create admin user
if not User.objects.filter(username='admin_screenshot').exists():
    user = User.objects.create_superuser('admin_screenshot', 'admin@example.com', 'admin_password123')
    print("Created superuser: admin_screenshot")
else:
    print("Superuser admin_screenshot already exists")

# Create normal user
if not User.objects.filter(username='user_screenshot').exists():
    user = User.objects.create_user('user_screenshot', 'user@example.com', 'user_password123')
    # Maybe need to create Client profile if your app requires it automatically or manually
    if not Client.objects.filter(user=user).exists():
        Client.objects.create(user=user, telephone='0123456789', adresse='123 rue test')
    print("Created normal user: user_screenshot")
else:
    print("Normal user user_screenshot already exists")
