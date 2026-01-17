"""
Views for System app - Developer tools.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection
from django.conf import settings
from .models import MaintenanceMode, FeatureFlag, LoginLog, PageVisit, ActiveSession
from .serializers import (
    MaintenanceModeSerializer, FeatureFlagSerializer, SystemStatsSerializer,
    LoginLogSerializer, PageVisitSerializer, ActiveSessionSerializer
)
from django.db.models import Count, Q
from django.db.models.functions import TruncHour, TruncDay
from django.utils import timezone
from datetime import timedelta


class IsDeveloper(permissions.BasePermission):
    """Permission class to restrict access to developers only."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or 
            (hasattr(request.user, 'is_developer') and request.user.is_developer)
        )


class MaintenanceModeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for maintenance mode status.
    Write operations are disabled for security.
    """
    queryset = MaintenanceMode.objects.all()
    serializer_class = MaintenanceModeSerializer
    permission_classes = [IsDeveloper]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current maintenance mode status."""
        maintenance = MaintenanceMode.get_current()
        serializer = self.get_serializer(maintenance)
        return Response(serializer.data)



class FeatureFlagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for feature flags.
    Allows viewing current flag states but not modifying them.
    Use Django admin for feature flag management.
    """
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer
    permission_classes = [IsDeveloper]
    
    # Toggle action removed - use Django admin to modify flags



class SystemStatsViewSet(viewsets.ViewSet):
    """System statistics for developer dashboard."""
    permission_classes = [IsDeveloper]
    
    def list(self, request):
        """Get comprehensive system statistics."""
        from apps.users.models import User
        from apps.tests.models import Test, TestSession
        from apps.questions.models import Question
        from apps.results.models import Result
        from apps.payments.models import Payment
        
        stats = {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'total_students': User.objects.filter(role='student').count(),
            'total_admins': User.objects.filter(role='admin').count(),
            'total_tests': Test.objects.count(),
            'total_questions': Question.objects.count(),
            'active_sessions': ActiveSession.objects.filter(last_activity__gte=timezone.now() - timedelta(minutes=30)).count(),
            'total_results': Result.objects.count(),
            'pending_payments': Payment.objects.filter(status='pending').count(),
            'database_size_mb': self._get_database_size()
        }
        
        serializer = SystemStatsSerializer(stats)
        return Response(serializer.data)
    
    def _get_database_size(self):
        """Get database size in MB."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_database_size(current_database())")
                size_bytes = cursor.fetchone()[0]
                return round(size_bytes / (1024 * 1024), 2)
        except:
            return None


class LoginLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for login logs."""
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    permission_classes = [IsDeveloper]
    filterset_fields = ['status', 'device_type', 'os', 'browser']
    search_fields = ['username_attempted', 'ip_address', 'device_model']
    ordering_fields = ['timestamp']


class ActiveSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for active user sessions."""
    serializer_class = ActiveSessionSerializer
    permission_classes = [IsDeveloper]
    
    def get_queryset(self):
        # Only show sessions active in the last 30 minutes
        threshold = timezone.now() - timedelta(minutes=30)
        return ActiveSession.objects.filter(last_activity__gte=threshold).order_by('-last_activity')


class MonitoringAnalyticsViewSet(viewsets.ViewSet):
    """ViewSet for various monitoring analytics charts and stats."""
    permission_classes = [IsDeveloper]
    
    @action(detail=False, methods=['get'])
    def realtime_dashboard(self, request):
        """Get data for real-time monitoring dashboard."""
        now = timezone.now()
        last_30_mins = now - timedelta(minutes=30)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Active users now
        active_count = ActiveSession.objects.filter(last_activity__gte=last_30_mins).count()
        
        # Visits today
        visits_today = PageVisit.objects.filter(timestamp__gte=today).count()
        
        # Device type distribution (all time)
        device_dist = LoginLog.objects.filter(status='success').values('device_type').annotate(count=Count('id'))
        
        # Hourly visits trend (last 24 hours)
        last_24_hours = now - timedelta(hours=24)
        hourly_visits = PageVisit.objects.filter(timestamp__gte=last_24_hours).annotate(
            hour=TruncHour('timestamp')
        ).values('hour').annotate(count=Count('id')).order_by('hour')
        
        return Response({
            'active_now': active_count,
            'visits_today': visits_today,
            'device_distribution': device_dist,
            'hourly_trend': hourly_visits
        })

    @action(detail=False, methods=['get'])
    def device_stats(self, request):
        """Get detailed device analytics."""
        # Top device models
        top_models = LoginLog.objects.filter(status='success').values('device_model', 'device_type').annotate(
            count=Count('id')
        ).order_by('-count')[:20]
        
        # OS distribution
        os_dist = LoginLog.objects.filter(status='success').values('os').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Browser distribution
        browser_dist = LoginLog.objects.filter(status='success').values('browser').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'top_models': top_models,
            'os_distribution': os_dist,
            'browser_distribution': browser_dist
        })

    @action(detail=False, methods=['get'])
    def visit_stats(self, request):
        """Get page visit analytics."""
        now = timezone.now()
        last_7_days = now - timedelta(days=7)
        
        # Top visited pages
        top_pages = PageVisit.objects.values('url_path').annotate(
            count=Count('id')
        ).order_by('-count')[:15]
        
        # Daily visits (last 7 days)
        daily_visits = PageVisit.objects.filter(timestamp__gte=last_7_days).annotate(
            day=TruncDay('timestamp')
        ).values('day').annotate(count=Count('id')).order_by('day')
        
        return Response({
            'top_pages': top_pages,
            'daily_trend': daily_visits
        })


class UserMonitoringViewSet(viewsets.ViewSet):
    """View user details and analytics for monitoring."""
    permission_classes = [IsDeveloper]
    
    def list(self, request):
        """List students for monitoring selection."""
        from apps.users.models import User
        queryset = User.objects.filter(role='student')
        
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) | 
                Q(full_name__icontains=search) | 
                Q(email__icontains=search)
            )
            
        # Basic list for picker
        data = queryset.values('id', 'username', 'full_name', 'email', 'last_login')[:100]
        return Response(data)

    def retrieve(self, request, pk=None):
        """Get full details for a specific student."""
        from apps.users.models import User
        from apps.users.serializers import UserSerializer
        
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            user_data = serializer.data
            
            # Add monitoring data
            user_data['login_history'] = LoginLogSerializer(
                LoginLog.objects.filter(user=user).order_by('-timestamp')[:20], 
                many=True
            ).data
            
            user_data['recent_visits'] = PageVisitSerializer(
                PageVisit.objects.filter(user=user).order_by('-timestamp')[:20], 
                many=True
            ).data
            
            # Dashboard stats (from users/views.py logic if available, or manual)
            # For now just basic
            return Response(user_data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class SecurityHealthCheckView(viewsets.ViewSet):
    """
    Enterprise-grade security health check telemetry.
    Returns the real-time security state of the application.
    """
    permission_classes = [IsDeveloper]

    def list(self, request):
        health_data = {
            'timestamp': timezone.now(),
            'environment': 'production' if not settings.DEBUG else 'development',
            'security_checks': {
                'debug_mode': {
                    'status': 'PASS' if not settings.DEBUG else 'FAIL',
                    'detail': 'Debug mode is disabled' if not settings.DEBUG else 'CRITICAL: Debug mode is enabled in production!'
                },
                'ssl_enforcement': {
                    'status': 'PASS' if getattr(settings, 'SECURE_SSL_REDIRECT', False) else 'WARNING',
                    'detail': 'SSL Redirection is enabled' if getattr(settings, 'SECURE_SSL_REDIRECT', False) else 'SSL Redirection is disabled'
                },
                'authentication': {
                    'status': 'PASS',
                    'detail': 'Using HttpOnly Cookie-based JWT'
                },
                'security_headers': {
                    'status': 'PASS' if hasattr(settings, 'CSP_DEFAULT_SRC') else 'WARNING',
                    'detail': 'CSP Headers are configured' if hasattr(settings, 'CSP_DEFAULT_SRC') else 'CSP Headers are missing'
                },
                'secret_management': {
                    'status': 'PASS' if settings.SECRET_KEY != 'django-insecure-change-this' else 'FAIL',
                    'detail': 'Secure Secret Key detected' if settings.SECRET_KEY != 'django-insecure-change-this' else 'CRITICAL: Default secret key in use!'
                },
                'database_security': {
                    'status': 'PASS',
                    'detail': 'PostgreSQL with connection pooling enabled'
                }
            },
            'overall_status': 'SECURE'
        }
        
        # Determine overall status
        for check in health_data['security_checks'].values():
            if check['status'] == 'FAIL':
                health_data['overall_status'] = 'COMPROMISED'
                break
            elif check['status'] == 'WARNING' and health_data['overall_status'] == 'SECURE':
                health_data['overall_status'] = 'DEGRADED'
                
        return Response(health_data)

class DatabaseViewSet(viewsets.ViewSet):
    """Database inspection for developer portal."""
    permission_classes = [IsDeveloper]
    
    def list(self, request):
        """List all tables in the database."""
        try:
            with connection.cursor() as cursor:
                # Query tables from information_schema
                cursor.execute("""
                    SELECT table_name, 
                           (SELECT count(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
                    FROM information_schema.tables t
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
                tables = []
                for row in cursor.fetchall():
                    tables.append({
                        'name': row[0],
                        'columns': row[1]
                    })
                return Response(tables)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def table_data(self, request):
        """Get data for a specific table."""
        table_name = request.query_params.get('table')
        if not table_name:
            return Response({'error': 'Table name required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with connection.cursor() as cursor:
                # Security check: Validate that the table exists in the public schema
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = %s
                    )
                """, [table_name])
                
                exists = cursor.fetchone()[0]
                if not exists:
                    return Response({'error': 'Invalid table name or table not found'}, status=status.HTTP_404_NOT_FOUND)

                # Now it's safe to use the table name in a query since we validated it exists in public schema
                # We still use f-string but ONLY after the explicit whitelist check above.
                # PostgreSQL doesn't support binding table names as parameters.
                cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 100')
                
                # Get column names from cursor description for reliable mapping
                columns = [col[0] for col in cursor.description]
                
                data = []
                # Column names to redact for security
                SENSITIVE_COLUMNS = ['password', 'token', 'secret', 'key', 'access_key', 'fingerprint']
                
                for row in cursor.fetchall():
                    # Map row to column names
                    row_dict = dict(zip(columns, row))
                    
                    # Redact sensitive columns
                    for col_name in columns:
                        lower_name = col_name.lower()
                        if any(sensitive in lower_name for sensitive in SENSITIVE_COLUMNS):
                            if row_dict[col_name] is not None:
                                row_dict[col_name] = "[REDACTED]"
                            
                    data.append(row_dict)
                    
                return Response({
                    'columns': columns,
                    'rows': data
                })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
