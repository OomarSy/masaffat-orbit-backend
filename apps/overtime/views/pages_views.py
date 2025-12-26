from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from ..filters import OvertimeFilter
from ..tables import OvertimeTable
from ..forms import OvertimeForm
from ..models import Overtime


from apps.core.views.pages_views import BaseCRUDView, BaseDeleteView, BaseListView


# Create your views here.
class ListOvertime(BaseListView):
    model = Overtime
    table_class = OvertimeTable
    filterset_class = OvertimeFilter
    view_name = "Overtime"
    add_url_name = 'attendance:overtime_create'
    segment = "overtime"


class DetailsOvertime(BaseCRUDView, DetailView):
    model = Overtime
    form_class = OvertimeForm
    view_name = "Overtime Details"
    details = True
    segment = "overtime"


class CreateOvertime(BaseCRUDView, CreateView):
    model = Overtime
    form_class = OvertimeForm
    template_name = 'generic/form.html'
    create = True
    success_url = reverse_lazy('attendance:overtime_list')
    view_name = "Create Overtime"
    segment = "overtime"

class UpdateOvertime(BaseCRUDView, UpdateView):
    model = Overtime
    form_class = OvertimeForm
    success_url = reverse_lazy('attendance:overtime_list')
    view_name = "Update Overtime"
    segment = "overtime"


class DeleteOvertime(BaseDeleteView):
    model = Overtime
    view_name = "Delete Overtime"
    segment = "overtime"