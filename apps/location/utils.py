from django.utils import timezone
from datetime import datetime

def parse_query_datetime(dt_str):
    if not dt_str:
        return None
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return dt
    except Exception:
        return None