from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import timezone
from apps.core.models import User
from datetime import timedelta
import json

class Command(BaseCommand):
    help = "Delete accounts with pending deletion request after 2 days of inactivity."

    def handle(self, *args, **options):
        keys = cache.keys("delete_request:*")
        for key in keys:
            try:
                data = json.loads(cache.get(key))
                user_id = data["user_id"]
                user = User.objects.get(id=user_id)
                
                if user.last_login is None or (timezone.now() - user.last_login) >= timedelta(days=2):
                    user.delete()
                    self.stdout.write(self.style.SUCCESS(f"Deleted user: {user.username}"))
                    cache.delete(key)
                else:
                    self.stdout.write(f"User {user.username} logged in recently. Skipping deletion.")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {key}: {e}"))
                cache.delete(key)
