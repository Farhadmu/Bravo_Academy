"""
Serializers for System app.
"""
from rest_framework import serializers
from .models import MaintenanceMode, FeatureFlag


class MaintenanceModeSerializer(serializers.ModelSerializer):
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True)
    
    class Meta:
        model = MaintenanceMode
        fields = [
            'id', 'is_active', 'target_roles', 'message',
            'updated_by', 'updated_by_username', 'updated_at', 'created_at'
        ]
        read_only_fields = ['id', 'updated_by', 'updated_at', 'created_at']


class FeatureFlagSerializer(serializers.ModelSerializer):
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = FeatureFlag
        fields = [
            'id', 'name', 'description', 'is_enabled', 'enabled_for_roles',
            'updated_by', 'updated_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SystemStatsSerializer(serializers.Serializer):
    """Statistics about the system."""
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_admins = serializers.IntegerField()
    total_tests = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    active_sessions = serializers.IntegerField()
    total_results = serializers.IntegerField()
    pending_payments = serializers.IntegerField()
    database_size_mb = serializers.FloatField(allow_null=True)
