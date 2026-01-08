"""
URL configuration for System app.
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    MaintenanceModeViewSet, 
    FeatureFlagViewSet, 
    SystemStatsViewSet,
    DatabaseViewSet,
    LoginLogViewSet,
    ActiveSessionViewSet,
    MonitoringAnalyticsViewSet,
    UserMonitoringViewSet
)

router = DefaultRouter()
router.register(r'maintenance', MaintenanceModeViewSet, basename='maintenance')
router.register(r'feature-flags', FeatureFlagViewSet, basename='feature-flags')
router.register(r'stats', SystemStatsViewSet, basename='stats')
router.register(r'database', DatabaseViewSet, basename='database')
router.register(r'login-logs', LoginLogViewSet, basename='login-logs')
router.register(r'active-sessions', ActiveSessionViewSet, basename='active-sessions')
router.register(r'analytics', MonitoringAnalyticsViewSet, basename='analytics')
router.register(r'user-monitoring', UserMonitoringViewSet, basename='user-monitoring')

urlpatterns = [
    path('', include(router.urls)),
]
