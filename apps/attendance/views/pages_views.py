from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from apps.core.views.pages_views import BaseCRUDView, BaseDeleteView, BaseListView
from apps.core.utils import api_response

from ..filters import EmployeeAttendanceFilter
from ..tables import EmployeeAttendanceTable
from ..services.attendance import EmployeeAttendanceService
from ..forms import EmployeeAttendanceForm
from ..models import EmployeeAttendance
from ..serializers import EmployeeAttendanceSerializer


# Employee Attendance Views
class ListEmployeeAttendance(BaseListView):
    model = EmployeeAttendance
    table_class = EmployeeAttendanceTable
    filterset_class = EmployeeAttendanceFilter
    view_name = "Employee Attendance"
    add_url_name = 'attendance:employeeattendance_create'


class DetailsEmployeeAttendance(BaseCRUDView, DetailView):
    model = EmployeeAttendance
    form_class = EmployeeAttendanceForm
    view_name = "Employee Attendance Details"
    details = True
    segment = "employeeattendance"


class CreateEmployeeAttendance(BaseCRUDView, CreateView):
    model = EmployeeAttendance
    form_class = EmployeeAttendanceForm
    template_name = 'generic/form.html'
    create = True
    success_url = reverse_lazy('attendance:employeeattendance_list')
    view_name = "Create Employee Attendance"
    segment = "employeeattendance"


class UpdateEmployeeAttendance(BaseCRUDView, UpdateView):
    model = EmployeeAttendance
    form_class = EmployeeAttendanceForm
    success_url = reverse_lazy('attendance:employeeattendance_list')
    view_name = "Update Employee Attendance"
    segment = "employeeattendance"


class DeleteEmployeeAttendance(BaseDeleteView):
    model = EmployeeAttendance
    view_name = "Delete Employee Attendance"
    segment = "employeeattendance"