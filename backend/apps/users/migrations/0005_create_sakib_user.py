from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin_user(apps, schema_editor):
    User = apps.get_model('users', 'User')
    
    # Create sakiburrahman user if it doesn't exist
    User.objects.get_or_create(
        username='sakiburrahman',
        defaults={
            'role': 'admin',
            'full_name': 'Sakibur Rahman',
            'email': 'admin@example.com',
            'password': make_password('sakiburrahman'),
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )

def remove_admin_user(apps, schema_editor):
    User = apps.get_model('users', 'User')
    User.objects.filter(username='sakiburrahman').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_device_tracking'),
    ]

    operations = [
        migrations.RunPython(create_admin_user, remove_admin_user),
    ]
