import os
import django
import sys

def seed():
    print("--- SEEDING START ---")
    try:
        # Ensure we are in the correct directory for relative imports if any
        sys.path.append(os.getcwd())
        
        settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.production')
        print(f"Using settings: {settings_module}")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        
        django.setup()
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        print("Database connection established.")

        # Admin User
        admin_username = 'admin'
        if not User.objects.filter(username=admin_username).exists():
            print(f"Creating superuser '{admin_username}'...")
            User.objects.create_superuser(
                username=admin_username, 
                email=os.getenv('SEED_ADMIN_EMAIL', 'admin@example.com'), 
                password=os.getenv('SEED_ADMIN_PASSWORD', 'admin123')
            )
            print(f"Superuser '{admin_username}' created successfully.")
        else:
            print(f"Superuser '{admin_username}' already exists.")

        # Student User
        student_username = 'student'
        if not User.objects.filter(username=student_username).exists():
            print(f"Creating student user '{student_username}'...")
            User.objects.create_user(
                username=student_username, 
                email=os.getenv('SEED_STUDENT_EMAIL', 'student@example.com'), 
                password=os.getenv('SEED_STUDENT_PASSWORD', 'student123'), 
                role='student'
            )
            print(f"Student user '{student_username}' created successfully.")
        else:
            print(f"Student user '{student_username}' already exists.")

        print("--- SEEDING COMPLETE ---")
        
    except Exception as e:
        print(f"!!! SEEDING ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    seed()
