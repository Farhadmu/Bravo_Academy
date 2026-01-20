from django.urls import path
from .views import current_maintenance

urlpatterns = [
    path('maintenance/current/', current_maintenance, name='maintenance-current'),
]
