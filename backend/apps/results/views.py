from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Result, PerformanceAnalytics
from .serializers import ResultSerializer, ResultDetailSerializer, PerformanceAnalyticsSerializer

class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ResultDetailSerializer
        return ResultSerializer

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user).select_related('test')

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]

        try:
            # Try by primary key first
            return queryset.get(pk=lookup_value)
        except (Result.DoesNotExist, ValueError):
            # If not found or invalid UUID for PK, try as session ID
            try:
                return queryset.get(test_session_id=lookup_value)
            except (Result.DoesNotExist, ValueError):
                from django.http import Http404
                raise Http404


class AnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for user analytics.
    Returns a single analytics object for the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """
        Return the analytics for the current user.
        Auto-creates analytics if it doesn't exist and recalculates from results.
        """
        # Get or create analytics for the user
        analytics, created = PerformanceAnalytics.objects.get_or_create(user=request.user)
        
        # If newly created or if the user requests a recalculation, rebuild from results
        if created:
            analytics.recalculate_from_results()
        
        # Serialize and return the single object (not a list)
        serializer = PerformanceAnalyticsSerializer(analytics)
        return Response(serializer.data)
