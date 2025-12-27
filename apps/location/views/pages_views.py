from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

from django.contrib.auth import get_user_model

User = get_user_model()


class EmployeeLocationsPageView(UserPassesTestMixin, TemplateView):
    template_name = "pages/location/map.html"
    segment = "location"
    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': '/dashboard/'},
            {'name': 'Locations', 'url': ''},
        ]
        context['unread_notifications_count'] = 0
        context['segment'] = self.segment
        return context


class EmployeeLocationsHistoryPageView(UserPassesTestMixin, TemplateView):
    template_name = "pages/location/history_map.html"
    segment = "location"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': '/dashboard/'},
            {'name': 'Locations History', 'url': ''},
        ]
        context['users'] = User.objects.all() 
        context['unread_notifications_count'] = 0
        context['segment'] = self.segment
        return context