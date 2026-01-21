from django.urls import path
from .views import current_maintenance, debug_s3

urlpatterns = [
    path('maintenance/current/', current_maintenance, name='maintenance-current'),
    path('debug-s3/', debug_s3, name='debug-s3'),
]
