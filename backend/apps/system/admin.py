"""
Admin interface for System app - Developer tools only.
"""
from django.contrib import admin
from .models import MaintenanceMode, FeatureFlag


@admin.register(MaintenanceMode)
class MaintenanceModeAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'target_roles', 'updated_at', 'updated_by')
    readonly_fields = ('updated_at', 'created_at')
    
    def has_module_permission(self, request):
        """Only developers can see this in admin."""
        return request.user.is_developer if hasattr(request.user, 'is_developer') else False
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_developer if hasattr(request.user, 'is_developer') else False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_developer if hasattr(request.user, 'is_developer') else False


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enabled', 'enabled_for_roles', 'updated_at')
    list_filter = ('is_enabled',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_module_permission(self, request):
        """Only developers can see this in admin."""
        return request.user.is_developer if hasattr(request.user, 'is_developer') else False
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_developer if hasattr(request.user, 'is_developer') else False
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_developer if hasattr(request.user, 'is_developer') else False
