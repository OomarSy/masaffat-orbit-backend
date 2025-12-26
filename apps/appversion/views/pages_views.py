from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from apps.core.views.pages_views import BaseCRUDView, BaseDeleteView, BaseListView

from ..filters import AppVersionFilter
from ..forms import AppVersionForm
from ..models import AppVersion
from ..tables import AppVersionTable


# AppVersion Views
class ListAppVersion(BaseListView):
    model = AppVersion
    table_class = AppVersionTable
    filterset_class = AppVersionFilter
    view_name = "AppVersion"
    add_url_name = 'appversion:appversion_create'
    segment = "appversion"


class DetailsAppVersion(BaseCRUDView, DetailView):
    model = AppVersion
    form_class = AppVersionForm
    view_name = "AppVersion Details"
    details = True
    segment = "appversion"


class CreateAppVersion(BaseCRUDView, CreateView):
    model = AppVersion
    form_class = AppVersionForm
    template_name = 'generic/form.html'
    create = True
    success_url = reverse_lazy('appversion:appversion_list')
    view_name = "Create AppVersion"
    segment = "appversion"

class UpdateAppVersion(BaseCRUDView, UpdateView):
    model = AppVersion
    form_class = AppVersionForm
    success_url = reverse_lazy('appversion:appversion_list')
    view_name = "Update AppVersion"
    segment = "appversion"


class DeleteAppVersion(BaseDeleteView):
    model = AppVersion
    view_name = "Delete AppVersion"
    segment = "appversion"