"""
Main URL configuration for the IQ Test Platform API.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint.
    Returns basic system information.
    """
    return Response({
        'status': 'healthy',
        'message': 'Defense Coaching Center & IQ Test Platform API is running',
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Health check
    path('api/health/', health_check, name='health-check'),
    
    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/tests/', include('apps.tests.urls')),
    path('api/questions/', include('apps.questions.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/results/', include('apps.results.urls')),
]

# Serve media files (Always serve in this specific setup for image visibility)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns

# Customize admin site
admin.site.site_header = "Defense Coaching Center & IQ Test Platform Admin"
admin.site.site_title = "IQ Test Platform Admin"
admin.site.index_title = "Welcome to the Administration Panel"
