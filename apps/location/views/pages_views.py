from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView


class UserLocationsPageView(UserPassesTestMixin, TemplateView):
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