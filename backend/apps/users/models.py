"""
User models for the IQ Test Platform.
Includes custom user with device tracking for preventing multi-device logins.
"""
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Manager for custom user model."""
    
    def create_user(self, username, password=None, **extra_fields):
        """Create and return a regular user."""
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with device tracking.
    Supports role-based access (admin, student, staff).
    """
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('developer', 'Developer'),  # Hidden superuser role for development
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # Profile fields
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Device tracking for one-device-per-user enforcement
    device_fingerprint = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    last_login_device = models.CharField(max_length=255, blank=True, null=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        app_label = 'users'
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Return user's full name or username."""
        return self.full_name if self.full_name else self.username
    
    def get_short_name(self):
        """Return username."""
        return self.username
    
    @property
    def is_admin(self):
        """Check if user is admin."""
        return self.role == 'admin' or self.is_superuser
    
    @property
    def is_student(self):
        """Check if user is student."""
        return self.role == 'student'
    
    # Developer Access Control
    is_developer = models.BooleanField(
        default=False, 
        help_text="Designates whether the user can access to Developer Portal."
    )
    
    def update_device_info(self, fingerprint, ip_address):
        """Update user's device fingerprint and IP."""
        self.device_fingerprint = fingerprint
        self.last_login_ip = ip_address
        self.last_login = timezone.now()
        self.save(update_fields=['device_fingerprint', 'last_login_ip', 'last_login'])
    
    def can_login_from_device(self, fingerprint):
        """
        Check if user can login from the given device.
        Returns True if:
        - No device fingerprint set yet (first login)
        - Device fingerprint matches stored fingerprint
        """
        if self.role == 'admin' or self.role == 'developer' or self.is_superuser:
            return True

        if not self.device_fingerprint:
            return True
        return self.device_fingerprint == fingerprint
