from django.conf import settings
from django.utils import timezone

def ensure_aware(dt):
    """
    يجعل datetime aware فقط إذا كان USE_TZ=True
    """
    if settings.USE_TZ and timezone.is_naive(dt):
        return timezone.make_aware(dt)
    return dt