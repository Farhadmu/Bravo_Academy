"""
System app for developer tools and maintenance mode.
"""
import uuid
from django.db import models
from django.conf import settings


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
