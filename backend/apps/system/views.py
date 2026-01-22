from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from decouple import config

@api_view(['GET'])
@permission_classes([AllowAny])
def current_maintenance(request):
    """
    Dummy maintenance endpoint to satisfy frontend calls.
    Always returns inactive status.
    """
    return Response({
        'is_active': False,
        'message': 'System is operating normally.'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def debug_s3(request):
    """
    Diagnostic endpoint to verify S3 configuration.
    """
    return Response({
        'status': 'deprecated',
        'message': 'This endpoint is no longer active.'
    })
