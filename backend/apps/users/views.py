"""
Views for user authentication and management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from .serializers import (
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    UserCreateSerializer
)
from apps.tests.models import Test

User = get_user_model()
import logging
logger = logging.getLogger(__name__)


# from apps.system.utils import log_login_attempt  # Removed apps.system


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Simplified login view - sets HttpOnly cookies for security.
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                access_token = response.data.get('access')
                refresh_token = response.data.get('refresh')
                
                if access_token:
                    response.set_cookie(
                        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                        value=access_token,
                        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                        path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                    )
                
                if refresh_token:
                    response.set_cookie(
                        key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                        value=refresh_token,
                        expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                        path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                    )
            return response
        except Exception as e:
            username = request.data.get('username')
            logger.warning(f"Login failed for user '{username}': {str(e)}")
            
            return Response({
                'error': 'Authentication Failed',
                'detail': 'Invalid username or password. Please try again.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class CookieTokenRefreshView(TokenRefreshView):
    """
    Custom TokenRefreshView that reads refresh token from cookie and sets new cookies.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        
        if refresh_token:
            data = request.data.copy()
            data['refresh'] = refresh_token
            request._full_data = data
            
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            if access_token:
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=access_token,
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                    path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                )
            
            if refresh_token:
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=refresh_token,
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                    path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                )
                
        return response


class LogoutView(viewsets.ViewSet):
    """Logout view that blacklists the refresh token."""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout user and blacklist refresh token."""
        try:
            refresh_token = request.data.get('refresh_token') or request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Clear device fingerprint on logout (Field deleted)
            # user = request.user
            # user.device_fingerprint = None
            # user.save(update_fields=['device_fingerprint'])
            
            response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
            response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
            response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    Only admins can create/delete users.
    Users can view/update their own profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create', 'destroy', 'list']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Use different serializer for create action."""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role. Hide developers and superusers from admins."""
        user = self.request.user
        if user.is_superuser or user.is_developer:
            return User.objects.all()
        if user.role == 'admin':
            # Strictly hide anyone with is_developer=True or role='developer'
            return User.objects.exclude(role='developer').exclude(is_developer=True).exclude(is_superuser=True)
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get or update current user profile."""
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password."""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reset_password(self, request, pk=None):
        """Admin action to reset any user's password."""
        user = self.get_object()
        new_password = request.data.get('password')
        
        if not new_password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(new_password)
        user.save()
        return Response({'detail': f'Password for {user.username} has been reset successfully.'})




class AdminDashboardViewSet(viewsets.ViewSet):
    """ViewSet for admin dashboard statistics."""
    permission_classes = [IsAdminUser]

    def list(self, request):
        """Get aggregated dashboard statistics."""
        # Stats
        total_students = User.objects.filter(role='student').count()
        total_tests = Test.objects.count()
        total_revenue = 0  # Payment system removed

        # Registration Stats (Last 7 days)
        last_7_days = timezone.now() - timedelta(days=7)
        registrations = User.objects.filter(
            role='student',
            created_at__gte=last_7_days
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        registration_data = []
        for i in range(7):
            date = (timezone.now() - timedelta(days=6-i)).date()
            count = next((item['count'] for item in registrations if item['date'] == date), 0)
            registration_data.append({
                'name': date.strftime('%a'),
                'students': count
            })

        # Recent Payments (Removed as payment app is deleted)
        # recent_payments = Payment.objects.filter(status='pending').select_related('user').order_by('-created_at')[:5]
        
        # from apps.payments.serializers import PaymentSerializer
        # payment_serializer = PaymentSerializer(recent_payments, many=True)

        return Response({
            'stats': {
                'total_students': total_students,
                'total_tests': total_tests,
                'pending_payments': 0,
                'total_revenue': total_revenue,
            },
            'registration_data': registration_data,
            'recent_payments': []
        })
