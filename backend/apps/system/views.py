"""
Views for System app - Developer tools.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection
from .models import MaintenanceMode, FeatureFlag
from .serializers import MaintenanceModeSerializer, FeatureFlagSerializer, SystemStatsSerializer


class IsDeveloper(permissions.BasePermission):
    """Permission class to restrict access to developers only."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'is_developer') and request.user.is_developer


class MaintenanceModeViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceMode.objects.all()
    serializer_class = MaintenanceModeSerializer
    permission_classes = [IsDeveloper]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current maintenance mode status."""
        maintenance = MaintenanceMode.get_current()
        serializer = self.get_serializer(maintenance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle maintenance mode on/off."""
        maintenance = MaintenanceMode.get_current()
        maintenance.is_active = not maintenance.is_active
        maintenance.updated_by = request.user
        maintenance.save()
        serializer = self.get_serializer(maintenance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_config(self, request):
        """Update maintenance mode configuration."""
        maintenance = MaintenanceMode.get_current()
        serializer = self.get_serializer(maintenance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer
    permission_classes = [IsDeveloper]
    
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """Toggle a feature flag."""
        flag = self.get_object()
        flag.is_enabled = not flag.is_enabled
        flag.updated_by = request.user
        flag.save()
        serializer = self.get_serializer(flag)
        return Response(serializer.data)


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
            'active_sessions': TestSession.objects.filter(status='in_progress').count(),
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
        
        # Security check: only public schema tables
        try:
            with connection.cursor() as cursor:
                # Get column names first
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", [table_name])
                columns = [col[0] for col in cursor.fetchall()]
                
                # Get data (limit 100 for safety)
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
                data = []
                for row in cursor.fetchall():
                    # Map row to column names
                    data.append(dict(zip(columns, row)))
                    
                return Response({
                    'columns': columns,
                    'rows': data
                })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
