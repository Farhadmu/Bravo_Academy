"""
URL configuration for System app.
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    MaintenanceModeViewSet, 
    FeatureFlagViewSet, 
    SystemStatsViewSet,
    DatabaseViewSet
)

router = DefaultRouter()
router.register(r'maintenance', MaintenanceModeViewSet, basename='maintenance')
router.register(r'feature-flags', FeatureFlagViewSet, basename='feature-flags')
router.register(r'stats', SystemStatsViewSet, basename='stats')
router.register(r'database', DatabaseViewSet, basename='database')

urlpatterns = [
    path('', include(router.urls)),
]
