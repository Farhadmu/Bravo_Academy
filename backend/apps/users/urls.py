"""
URL patterns for user authentication.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView, 
    CookieTokenRefreshView, 
    LogoutView, 
    UserViewSet, 
    AdminDashboardViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'dashboard-stats', AdminDashboardViewSet, basename='dashboard-stats')

urlpatterns = [
    # JWT Authentication
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view({'post': 'logout'}), name='logout'),
    
    # Include router URLs
    path('', include(router.urls)),
]
