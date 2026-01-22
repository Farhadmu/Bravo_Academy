from django.urls import path
from .views import current_maintenance, debug_s3, emergency_access, debug_kill_connections

urlpatterns = [
    path('maintenance/current/', current_maintenance, name='maintenance-current'),
    path('debug-s3/', debug_s3, name='debug-s3'),
    path('debug-emergency/', emergency_access, name='debug-emergency'),
    path('debug-kill/', debug_kill_connections, name='debug-kill'),
]
