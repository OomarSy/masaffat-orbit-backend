from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from apps.core.views.pages_views import BaseCRUDView, BaseDeleteView, BaseListView

from ..filters import AndroidAppReleaseFilter
from ..forms import AndroidAppReleaseForm
from ..models import AndroidAppRelease
from ..tables import AndroidAppReleaseTable


# AndroidAppRelease Views
class ListAndroidAppRelease(BaseListView):
    model = AndroidAppRelease
    table_class = AndroidAppReleaseTable
    filterset_class = AndroidAppReleaseFilter
    view_name = "Android App Release"
    add_url_name = 'appversion:androidapprelease_create'
    segment = "androidapprelease"


class DetailsAndroidAppRelease(BaseCRUDView, DetailView):
    model = AndroidAppRelease
    form_class = AndroidAppReleaseForm
    view_name = "Android App Release Details"
    details = True
    segment = "androidapprelease"


class CreateAndroidAppRelease(BaseCRUDView, CreateView):
    model = AndroidAppRelease
    form_class = AndroidAppReleaseForm
    template_name = 'generic/form.html'
    create = True
    success_url = reverse_lazy('appversion:androidapprelease_list')
    view_name = "Create Android App Release"
    segment = "androidapprelease"

class UpdateAndroidAppRelease(BaseCRUDView, UpdateView):
    model = AndroidAppRelease
    form_class = AndroidAppReleaseForm
    success_url = reverse_lazy('appversion:androidapprelease_list')
    view_name = "Update Android App Release"
    segment = "androidapprelease"


class DeleteAndroidAppRelease(BaseDeleteView):
    model = AndroidAppRelease
    view_name = "Delete Android App Release"
    segment = "androidapprelease"