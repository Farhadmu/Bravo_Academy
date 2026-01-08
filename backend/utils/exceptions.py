from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django Rest Framework.
    Provides standardized error responses and logs server errors.
    """
    # Call standard DRF exception handler first
    response = exception_handler(exc, context)

    if response is None:
        # This is a server-side error (500) that DRF didn't handle
        logger.error(f"Server Error: {str(exc)}", exc_info=True)
        
        return Response({
            'error': 'Internal Server Error',
            'detail': 'An unexpected error occurred. Please try again later.',
            'status_code': 500
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Standardize the response structure
    custom_data = {
        'error': response.data.get('detail') or response.data.get('error') or 'Error',
        'status_code': response.status_code,
        'detail': response.data
    }
    
    # If there are field-specific errors, they'll be in response.data
    # We keep them in 'detail' for frontend to parse
    
    response.data = custom_data
    return response
