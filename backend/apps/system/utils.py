"""
Utilities for system monitoring and analytics.
"""
from user_agents import parse
from django.utils import timezone
from .models import LoginLog, PageVisit, ActiveSession


def get_client_ip(request):
    """Extract client IP from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_device_info(user_agent_string):
    """
    Parse User-Agent string to extract device model, type, browser, and OS.
    Returns: (device_model, device_type, browser, os)
    """
    if not user_agent_string:
        return ("Unknown", "unknown", "Unknown", "Unknown")
        
    ua = parse(user_agent_string)
    
    # Extract Device Model
    device_model = ua.device.model or ua.device.family or "Unknown"
    if device_model == "Other":
        device_model = "Unknown"
        
    # Extract Device Type
    if ua.is_mobile:
        device_type = 'mobile'
    elif ua.is_tablet:
        device_type = 'tablet'
    elif ua.is_pc:
        # Check if it looks like a laptop/desktop (approximation)
        device_type = 'desktop' # Default to desktop if PC
    else:
        device_type = 'unknown'
        
    # Browser
    browser = f"{ua.browser.family} {ua.browser.version_string}"
    
    # OS
    os = f"{ua.os.family} {ua.os.version_string}"
    
    return (device_model, device_type, browser, os)


def log_login_attempt(request, user=None, username_attempted=None, status='success', failure_reason=None):
    """Log a login attempt."""
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    ip_address = get_client_ip(request)
    device_fingerprint = request.data.get('device_fingerprint', '') if hasattr(request, 'data') else ''
    
    device_model, device_type, browser, os = parse_device_info(user_agent_string)
    
    LoginLog.objects.create(
        user=user,
        username_attempted=username_attempted or (user.username if user else "Unknown"),
        ip_address=ip_address,
        device_fingerprint=device_fingerprint,
        device_model=device_model,
        device_type=device_type,
        browser=browser,
        os=os,
        status=status,
        failure_reason=failure_reason,
        user_agent=user_agent_string
    )


def update_active_session(request, user):
    """
    Create or update an active session record for the user.
    """
    session_key = getattr(request.session, 'session_key', None)
    if not session_key:
        return
        
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    ip_address = get_client_ip(request)
    device_model, device_type, browser, os = parse_device_info(user_agent_string)
    
    ActiveSession.objects.update_or_create(
        session_key=session_key,
        defaults={
            'user': user,
            'ip_address': ip_address,
            'device_model': device_model,
            'device_type': device_type,
            'browser': browser,
            'os': os,
            'current_page': request.path,
            'last_activity': timezone.now()
        }
    )


def log_page_visit(request, user=None):
    """Log a page visit."""
    session_key = getattr(request.session, 'session_key', 'anon-session')
    ip_address = get_client_ip(request)
    
    PageVisit.objects.create(
        user=user,
        session_id=session_key,
        url_path=request.path,
        ip_address=ip_address,
        device_fingerprint='', # Could be passed from frontend if needed
        referrer=request.META.get('HTTP_REFERER', '')
    )
    
    # Also update active session if user is logged in
    if user and user.is_authenticated:
        update_active_session(request, user)
