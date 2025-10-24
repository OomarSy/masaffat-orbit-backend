from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from apps.core.models import User
from apps.location.models import UserLocation

@login_required
def dashboard(request):
    offline_threshold = timezone.now() - timedelta(minutes=5)

    total_users = User.objects.filter(is_superuser=False).count()

    locations = UserLocation.objects.select_related('user').all()

    online_users = locations.filter(updated_at__gte=offline_threshold).count()
    offline_users = total_users - online_users

    context = {
        'segment': 'dashboard',
        'total_users': total_users,
        'online_users': online_users,
        'offline_users': offline_users,
    }
    return render(request, 'pages/dashboard/dashboard.html', context)
