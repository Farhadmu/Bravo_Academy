"""
Middleware for maintenance mode enforcement.
"""
from django.http import JsonResponse
from apps.system.models import MaintenanceMode


class MaintenanceModeMiddleware:
    """
    Middleware to check maintenance mode before processing requests.
    Blocks users with specific roles during maintenance.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Allow OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return self.get_response(request)
        
        # Allow unauthenticated requests to pass through
        # Maintenance check happens at login
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Skip maintenance check for static files and admin
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return self.get_response(request)
        
        # Check if maintenance mode is active and user's role is blocked
        try:
            maintenance = MaintenanceMode.get_current()
            if maintenance.is_role_blocked(request.user.role):
                return JsonResponse({
                    'error': 'Maintenance Mode',
                    'message': maintenance.message,
                    'detail': 'The system is currently under maintenance for your role.'
                }, status=503)
        except Exception:
            # If anything goes wrong with maintenance check, allow request through
            pass
        
        response = self.get_response(request)
        return response
