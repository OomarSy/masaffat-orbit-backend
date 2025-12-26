from django.conf import settings
from django.utils import timezone

def ensure_aware(dt):
    """
    Converts the datetime object to a timezone-aware one only when USE_TZ is enabled.
    """
    if settings.USE_TZ and timezone.is_naive(dt):
        return timezone.make_aware(dt)
    return dt