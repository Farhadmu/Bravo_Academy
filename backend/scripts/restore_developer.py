import os
import django
import sys
from django.contrib.auth import get_user_model

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

User = get_user_model()

def restore_developer():
    username = 'developer'
    password = 'developersakiburrahman'
    
    # Check if exists
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists. Updating credentials.")
        user = User.objects.get(username=username)
    else:
        print(f"Creating user '{username}'...")
        user = User(username=username)

    user.set_password(password)
    user.role = 'developer'
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.is_developer = True  # Explicit flag if used in other logic
    user.full_name = "System Developer"
    user.save()
    
    print(f"Successfully restored user '{username}' with superuser privileges.")

if __name__ == '__main__':
    try:
        restore_developer()
    except Exception as e:
        print(f"Error restoring developer: {e}")
