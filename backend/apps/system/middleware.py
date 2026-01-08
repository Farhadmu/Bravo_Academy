"""
Middleware for maintenance mode enforcement and system monitoring.
"""
from django.http import JsonResponse
from django.contrib.auth import logout
from apps.system.models import MaintenanceMode
from apps.system.utils import log_page_visit


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
                # Log out the user to invalidate their session
                logout(request)
                
                return JsonResponse({
                    'error': 'Maintenance Mode',
                    'message': maintenance.message,
                    'detail': 'You have been logged out because the system is under maintenance for your role.',
                    'logout': True  # Signal to frontend to clear auth state
                }, status=401)  # Use 401 to trigger frontend logout handling
        except Exception:
            # If anything goes wrong with maintenance check, allow request through
            pass
        
        response = self.get_response(request)
        return response


class MonitoringMiddleware:
    """
    Middleware to log page visits and track active sessions for the developer portal.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Skip logging for static files, media, and common internal assets
        if any(request.path.startswith(prefix) for prefix in ['/static/', '/media/', '/_next/', '/favicon.ico']):
            return self.get_response(request)
            
        # Get response first so we have the full context
        response = self.get_response(request)
        
        # Only log successful or not-found GET/POST requests
        if response.status_code in [200, 201, 404] and request.method in ['GET', 'POST']:
            try:
                # Log the visit (will also update active session if authenticated)
                log_page_visit(request, user=request.user if request.user.is_authenticated else None)
            except Exception:
                # Silently fail monitoring if something goes wrong
                pass
                
        return response
