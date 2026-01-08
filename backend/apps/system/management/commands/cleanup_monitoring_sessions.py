from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.system.models import ActiveSession

class Command(BaseCommand):
    help = 'Cleans up stale active session records older than 24 hours.'

    def handle(self, *args, **options):
        # We keep sessions for a bit longer than the 30-min "active" window
        # to allow for some historical analysis if needed, but 24 hours is a safe
        # cutoff to prevent table bloat.
        cutoff = timezone.now() - timedelta(hours=24)
        count, _ = ActiveSession.objects.filter(last_activity__lt=cutoff).delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} stale active session records')
        )
