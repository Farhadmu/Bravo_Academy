from django.db import migrations
from django.contrib.auth.hashers import make_password

def setup_developer(apps, schema_editor):
    User = apps.get_model('users', 'User')
    username = 'developer'
    password = 'developersakiburrahman'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create(
            username=username,
            password=make_password(password),
            role='developer',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_developer=True,
            full_name="System Developer"
        )
    else:
        # Update existing user to ensure credentials match
        user = User.objects.get(username=username)
        user.password = make_password(password)
        user.role = 'developer'
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_developer = True
        user.save()

def reverse_setup_developer(apps, schema_editor):
    # We won't delete the user in reverse to prevent data loss, 
    # but we could downgrade permissions if needed.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_role'),
    ]

    operations = [
        migrations.RunPython(setup_developer, reverse_setup_developer),
    ]
