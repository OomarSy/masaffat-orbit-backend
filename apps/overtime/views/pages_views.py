from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from ..filters import EmployeeOvertimeFilter
from ..tables import EmployeeOvertimeTable
from ..forms import EmployeeOvertimeForm
from ..models import EmployeeOvertime


from apps.core.views.pages_views import BaseCRUDView, BaseDeleteView, BaseListView


# Create your views here.
class ListEmployeeOvertime(BaseListView):
    model = EmployeeOvertime
    table_class = EmployeeOvertimeTable
    filterset_class = EmployeeOvertimeFilter
    view_name = "EmployeeOvertime"
    add_url_name = 'overtime:employeeovertime_create'
    segment = "employeeovertime"


class DetailsEmployeeOvertime(BaseCRUDView, DetailView):
    model = EmployeeOvertime
    form_class = EmployeeOvertimeForm
    view_name = "Employee Overtime Details"
    details = True
    segment = "employeeovertime"
    

class CreateEmployeeOvertime(BaseCRUDView, CreateView):
    model = EmployeeOvertime
    form_class = EmployeeOvertimeForm
    template_name = 'generic/form.html'
    create = True
    success_url = reverse_lazy('overtime:employeeovertime_list')
    view_name = "Create Overtime"
    segment = "employeeovertime"


class UpdateEmployeeOvertime(BaseCRUDView, UpdateView):
    model = EmployeeOvertime
    form_class = EmployeeOvertimeForm
    success_url = reverse_lazy('overtime:employeeovertime_list')
    view_name = "Update Overtime"
    segment = "employeeovertime"


class DeleteEmployeeOvertime(BaseDeleteView):
    model = EmployeeOvertime
    view_name = "Delete Overtime"
    segment = "employeeovertime"