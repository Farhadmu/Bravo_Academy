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
        admin_password = os.getenv('SEED_ADMIN_PASSWORD')
        if not admin_password:
             raise ValueError("SEED_ADMIN_PASSWORD environment variable is NOT set.")
             
        if not User.objects.filter(username=admin_username).exists():
            print(f"Creating superuser '{admin_username}'...")
            User.objects.create_superuser(
                username=admin_username, 
                email=os.getenv('SEED_ADMIN_EMAIL', 'admin@example.com'), 
                password=admin_password
            )
            print(f"Superuser '{admin_username}' created successfully.")
        else:
            print(f"Superuser '{admin_username}' already exists.")

        # Student User
        student_username = 'student'
        student_password = os.getenv('SEED_STUDENT_PASSWORD')
        if not student_password:
            raise ValueError("SEED_STUDENT_PASSWORD environment variable is NOT set.")

        if not User.objects.filter(username=student_username).exists():
            print(f"Creating student user '{student_username}'...")
            User.objects.create_user(
                username=student_username, 
                email=os.getenv('SEED_STUDENT_EMAIL', 'student@example.com'), 
                password=student_password, 
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
