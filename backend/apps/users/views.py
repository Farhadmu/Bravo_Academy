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
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from .serializers import (
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    UserCreateSerializer
)
from utils.device_tracking import get_client_ip
from apps.tests.models import Test
from apps.payments.models import Payment, UserTestAccess

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view with device tracking.
    Checks if user can login from the device and updates device info.
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        # Proceed with normal login first to verify credentials
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            # Check if user exists but password failed
            username = request.data.get('username')
            if username:
                user_exists = User.objects.filter(username=username).exists()
                if user_exists:
                    return Response({
                        'error': 'Incorrect Password',
                        'detail': 'The password you entered is incorrect. Please try again or contact the admin.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({
                        'error': 'User Not Found',
                        'detail': f'No account found with the username "{username}". Please check for typos.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            raise e
        if response.status_code == 200:
            # Login successful, now check device fingerprint and maintenance mode
            username = request.data.get('username', '')
            device_fingerprint = request.data.get('device_fingerprint', '')
            
            try:
                user = User.objects.get(username=username)
                
                # Check for Maintenance Mode
                from apps.system.models import MaintenanceMode
                maintenance = MaintenanceMode.get_current()
                if maintenance.is_role_blocked(user.role):
                    return Response({
                        'error': 'Maintenance Mode',
                        'message': maintenance.message,
                        'detail': 'The system is currently under maintenance for your role.'
                    }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

                # Check if user can login from this device
                if not user.can_login_from_device(device_fingerprint):
                    return Response({
                        'error': 'This ID is already logged in on another device. You cannot login using a different device with the same ID.'
                    }, status=status.HTTP_403_FORBIDDEN)
                
                # Update device info
                ip_address = get_client_ip(request)
                user.update_device_info(device_fingerprint, ip_address)
                
            except User.DoesNotExist:
                # Should not happen as super().post() was successful
                pass
            except Exception as e:
                print(f"Error updating device info: {e}")
        
        return response


class LogoutView(viewsets.ViewSet):
    """Logout view that blacklists the refresh token."""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout user and blacklist refresh token."""
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Clear device fingerprint on logout
            user = request.user
            user.device_fingerprint = None
            user.save(update_fields=['device_fingerprint'])
            
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
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
        """Filter queryset based on user role. Hide developers from admins."""
        user = self.request.user
        if user.is_developer:
            return User.objects.all()
        if user.is_admin:
            return User.objects.exclude(role='developer')
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

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reset_device(self, request, pk=None):
        """Admin action to reset a user's device fingerprint."""
        user = self.get_object()
        user.device_fingerprint = None
        user.save()
        return Response({'detail': f'Device fingerprint for {user.username} has been cleared.'})


class AdminDashboardViewSet(viewsets.ViewSet):
    """ViewSet for admin dashboard statistics."""
    permission_classes = [IsAdminUser]

    def list(self, request):
        """Get aggregated dashboard statistics."""
        # Stats
        total_students = User.objects.filter(role='student').count()
        total_tests = Test.objects.count()
        pending_payments = Payment.objects.filter(status='pending').count()
        total_revenue = Payment.objects.filter(status='verified').aggregate(Sum('amount'))['amount__sum'] or 0

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

        # Recent Payments
        recent_payments = Payment.objects.filter(status='pending').select_related('user').order_by('-created_at')[:5]
        
        from apps.payments.serializers import PaymentSerializer
        payment_serializer = PaymentSerializer(recent_payments, many=True)

        return Response({
            'stats': {
                'total_students': total_students,
                'total_tests': total_tests,
                'pending_payments': pending_payments,
                'total_revenue': total_revenue,
            },
            'registration_data': registration_data,
            'recent_payments': payment_serializer.data
        })
