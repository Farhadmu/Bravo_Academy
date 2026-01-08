"""
System app for developer tools and maintenance mode.
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class MaintenanceMode(models.Model):
    """
    Control system maintenance mode to lock specific user roles.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=False)
    
    # JSON list of roles to block: ['student', 'admin', 'staff']
    # Developer role is never blocked
    target_roles = models.JSONField(
        default=list,
        help_text="List of roles to block during maintenance"
    )
    
    message = models.TextField(
        default="System is under maintenance. Please try again later.",
        help_text="Custom message to show blocked users"
    )
    
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='maintenance_updates'
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'system'
        db_table = 'maintenance_mode'
        verbose_name = 'Maintenance Mode'
        verbose_name_plural = 'Maintenance Modes'
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"Maintenance Mode - {status}"
    
    @classmethod
    def get_current(cls):
        """Get the current maintenance mode config (singleton pattern)."""
        obj, created = cls.objects.get_or_create(
            pk='00000000-0000-0000-0000-000000000001',
            defaults={
                'is_active': False,
                'target_roles': ['student', 'admin'],
                'message': 'System is under maintenance. Please try again later.'
            }
        )
        return obj
    
    def is_role_blocked(self, role):
        """Check if a specific role is blocked."""
        if role == 'developer':
            return False  # Never block developers
        return self.is_active and role in self.target_roles


class FeatureFlag(models.Model):
    """
    Feature flags for toggling features without code deployment.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique feature identifier (e.g., 'new_dashboard')"
    )
    description = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=False)
    
    # Optional: Limit to specific roles
    enabled_for_roles = models.JSONField(
        default=list,
        blank=True,
        help_text="If specified, only these roles can access the feature"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    
    class Meta:
        app_label = 'system'
        db_table = 'feature_flags'
        verbose_name = 'Feature Flag'
        verbose_name_plural = 'Feature Flags'
        ordering = ['name']
    
    def __str__(self):
        status = "ON" if self.is_enabled else "OFF"
        return f"{self.name} [{status}]"
    
    def is_enabled_for_user(self, user):
        """Check if feature is enabled for specific user."""
        if not self.is_enabled:
            return False
        if not self.enabled_for_roles:
            return True  # Enabled for all if no role restriction
        return user.role in self.enabled_for_roles


class LoginLog(models.Model):
    """Track all login attempts with detailed device information."""
    
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    DEVICE_TYPE_CHOICES = [
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('unknown', 'Unknown'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    username_attempted = models.CharField(max_length=255, help_text="Username used in login attempt")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    ip_address = models.GenericIPAddressField()
    device_fingerprint = models.CharField(max_length=255, blank=True)
    device_model = models.CharField(max_length=255, blank=True, help_text="e.g., iPhone 14 Pro, HP EliteBook 840")
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES, default='unknown')
    browser = models.CharField(max_length=100, blank=True, help_text="e.g., Chrome 120, Safari 17")
    os = models.CharField(max_length=100, blank=True, help_text="e.g., Android 13, Windows 11")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    failure_reason = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.TextField(help_text="Raw user agent string")
    
    class Meta:
        app_label = 'system'
        db_table = 'login_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.username_attempted} - {self.status} - {self.timestamp}"


class PageVisit(models.Model):
    """Track page visits for analytics."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=255, db_index=True, help_text="Session identifier")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    url_path = models.CharField(max_length=500, help_text="e.g., /dashboard, /tests/123")
    page_title = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField()
    device_fingerprint = models.CharField(max_length=255, blank=True)
    referrer = models.CharField(max_length=500, blank=True, null=True)
    time_spent = models.IntegerField(default=0, help_text="Seconds spent on page")
    
    class Meta:
        app_label = 'system'
        db_table = 'page_visits'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['session_id']),
            models.Index(fields=['url_path']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"{user_str} - {self.url_path} - {self.timestamp}"


class ActiveSession(models.Model):
    """Track currently active user sessions."""
    
    DEVICE_TYPE_CHOICES = [
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('unknown', 'Unknown'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, unique=True, db_index=True)
    login_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True, db_index=True)
    ip_address = models.GenericIPAddressField()
    device_model = models.CharField(max_length=255, blank=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES, default='unknown')
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    current_page = models.CharField(max_length=500, blank=True)
    
    class Meta:
        app_label = 'system'
        db_table = 'active_sessions'
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['-last_activity']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.session_key}"
    
    @property
    def session_duration(self):
        """Calculate session duration in seconds."""
        return (timezone.now() - self.login_time).total_seconds()
    
    @property
    def is_active(self):
        """Check if session is still active (activity within last 30 minutes)."""
        inactive_threshold = timezone.now() - timezone.timedelta(minutes=30)
        return self.last_activity > inactive_threshold
