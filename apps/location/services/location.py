from django.utils import timezone
from apps.location.models import EmployLocation, EmployLocationHistory
from datetime import timedelta


class EmployLocationService:
    @staticmethod
    def update_user_location(user, latitude, longitude):
        location, created = EmployLocation.objects.get_or_create(user=user)
        location.latitude = latitude
        location.longitude = longitude
        location.updated_at = timezone.now()
        location.save()

        EmployLocationHistory.objects.create(
            user=user,
            latitude=latitude,
            longitude=longitude,
        )

        return location

    @staticmethod
    def get_all_user_locations(offline_threshold_minutes=5):
        """
        Return all users with their latest coordinates.
        Adds an 'is_online' attribute based on the last updated timestamp.
        """
        locations = EmployLocation.objects.select_related("user").all()
        now = timezone.now()

        for loc in locations:
            if loc.updated_at:
                loc.is_online = (now - loc.updated_at) <= timedelta(minutes=offline_threshold_minutes)
            else:
                loc.is_online = False

        return locations


    @staticmethod
    def get_all_locations():
        return EmployLocation.objects.select_related('user').all()
