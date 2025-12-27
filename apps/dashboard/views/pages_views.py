from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from datetime import timedelta

from apps.location.models import EmployLocation
from apps.users.models import User

@login_required
def dashboard(request):
    offline_threshold = timezone.now() - timedelta(minutes=5)

    all_users = User.objects.filter(is_superuser=False)
    total_users = all_users.count()

    locations = EmployLocation.objects.select_related('user').all()
    online_users_ids = locations.filter(updated_at__gte=offline_threshold).values_list('user_id', flat=True)

    for user in all_users:
        user.is_active = user.id in online_users_ids

    online_users = sum(user.is_active for user in all_users)
    offline_users = total_users - online_users

    context = {
        'segment': 'dashboard',
        'all_users': all_users,
        'total_users': total_users,
        'online_users': online_users,
        'offline_users': offline_users,
    }
    return render(request, 'pages/dashboard/dashboard.html', context)
