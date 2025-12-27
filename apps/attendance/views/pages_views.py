from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from apps.core.views.pages_views import BaseCRUDView, BaseDeleteView, BaseListView
from apps.core.utils import api_response

from ..filters import AttendanceFilter
from ..tables import AttendanceTable
from ..services.attendance import AttendanceService
from ..forms import AttendanceForm
from ..models import Attendance
from ..serializers import AttendanceSerializer


# Attendance Views
class ListAttendance(BaseListView):
    model = Attendance
    table_class = AttendanceTable
    filterset_class = AttendanceFilter
    view_name = "Attendance"
    add_url_name = 'attendance:attendance_create'


class DetailsAttendance(BaseCRUDView, DetailView):
    model = Attendance
    form_class = AttendanceForm
    view_name = "Attendance Details"
    details = True
    segment = "attendance"


class CreateAttendance(BaseCRUDView, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'generic/form.html'
    create = True
    success_url = reverse_lazy('attendance:attendance_list')
    view_name = "Create Attendance"
    segment = "attendance"


class UpdateAttendance(BaseCRUDView, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    success_url = reverse_lazy('attendance:attendance_list')
    view_name = "Update Attendance"
    segment = "attendance"


class DeleteAttendance(BaseDeleteView):
    model = Attendance
    view_name = "Delete Attendance"
    segment = "attendance"