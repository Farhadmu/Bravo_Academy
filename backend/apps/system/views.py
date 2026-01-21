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
    # Check variables from settings (which loaded from env)
    access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
    endpoint = getattr(settings, 'AWS_S3_ENDPOINT_URL', None)
    
    return Response({
        'storage_backend': getattr(settings, 'DEFAULT_FILE_STORAGE', 'Unknown'),
        'aws_access_key_id': 'PRESENT' if access_key else 'MISSING',
        'aws_secret_access_key': 'PRESENT' if secret_key else 'MISSING',
        'aws_storage_bucket_name': bucket if bucket else 'MISSING',
        'aws_s3_endpoint_url': endpoint if endpoint else 'MISSING',
        'aws_querystring_auth': getattr(settings, 'AWS_QUERYSTRING_AUTH', 'Unknown'),
        'aws_s3_custom_domain': getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'None'),
    }, status=status.HTTP_200_OK)
