"""
Serializers for System app.
"""
from rest_framework import serializers
from .models import MaintenanceMode, FeatureFlag, LoginLog, PageVisit, ActiveSession


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


class LoginLogSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    
    class Meta:
        model = LoginLog
        fields = [
            'id', 'user', 'user_username', 'username_attempted', 'timestamp',
            'ip_address', 'device_fingerprint', 'device_model', 'device_type',
            'browser', 'os', 'status', 'failure_reason', 'user_agent'
        ]
        read_only_fields = fields


class PageVisitSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    
    class Meta:
        model = PageVisit
        fields = [
            'id', 'user', 'user_username', 'session_id', 'timestamp',
            'url_path', 'page_title', 'ip_address', 'device_fingerprint',
            'referrer', 'time_spent'
        ]
        read_only_fields = fields


class ActiveSessionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    duration = serializers.FloatField(source='session_duration', read_only=True)
    is_session_active = serializers.BooleanField(source='is_active', read_only=True)
    
    class Meta:
        model = ActiveSession
        fields = [
            'id', 'user', 'user_username', 'session_key', 'login_time',
            'last_activity', 'ip_address', 'device_model', 'device_type',
            'browser', 'os', 'current_page', 'duration', 'is_session_active'
        ]
        read_only_fields = fields


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
