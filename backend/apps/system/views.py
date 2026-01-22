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
    
@api_view(['POST'])
@permission_classes([AllowAny])
def emergency_access(request):
    """
    Emergency endpoint to reset password or create user.
    Internal use only - secured by hardcoded secret.
    """
    secret = request.data.get('secret')
    if secret != 'BravoAlpha2026!':  # Hardcoded safety latch
        return Response({'error': 'Unauthorized'}, status=403)
        
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Missing credentials'}, status=400)
        
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.email = f"{username}@example.com"
        
        user.set_password(password)
        user.save()
        
        return Response({
            'status': 'success',
            'action': 'created' if created else 'updated',
            'username': username
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def debug_kill_connections(request):
    """
    Emergency Defibrillator: Kill all other connections to free up the pool.
    """
    secret = request.data.get('secret')
    if secret != 'BravoAlpha2026!':
        return Response({'error': 'Unauthorized'}, status=403)
        
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT pg_terminate_backend(pid) 
                FROM pg_stat_activity 
                WHERE pid <> pg_backend_pid() 
                AND datname = current_database()
            """)
            count = cursor.rowcount
        return Response({'status': 'success', 'killed_connections': count})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
