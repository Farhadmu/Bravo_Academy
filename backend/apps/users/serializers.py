"""
Serializers for user authentication and management.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'phone', 'role', 
                  'is_active', 'created_at', 'updated_at', 'last_login')
        read_only_fields = ('id', 'role', 'is_active', 'created_at', 'updated_at', 'last_login')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with user information."""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    
    def validate_old_password(self, value):
        """Verify old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        """Validate password complexity using Django's built-in validators."""
        user = self.context['request'].user
        try:
            validate_password(value, user)
        except Exception as e:
            # Re-raise as a proper serializer validation error if needed
            # (DRF usually handles Django's ValidationError, but this is more explicit)
            raise serializers.ValidationError(list(e.messages) if hasattr(e, 'messages') else str(e))
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users (admin only)."""
    
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    username = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'full_name', 'phone', 'role', 'is_active')
    
    def create(self, validated_data):
        """Create user with hashed password and auto-generated username."""
        if 'username' not in validated_data or not validated_data['username']:
            full_name = validated_data.get('full_name', '')
            if not full_name:
                # If no full name, try to use email prefix
                email = validated_data.get('email', '')
                if email:
                    base_username = email.split('@')[0]
                else:
                    raise serializers.ValidationError({"full_name": "Full name is required to auto-generate username."})
            else:
                import re
                base_username = full_name.lower()
                base_username = re.sub(r'[^a-z0-9]', '', base_username)
            
            if not base_username:
                base_username = "user"
                
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            validated_data['username'] = username

        # If password is not provided, use username as password
        if 'password' not in validated_data or not validated_data['password']:
            validated_data['password'] = validated_data.get('username')

        user = User.objects.create_user(**validated_data)
        return user
