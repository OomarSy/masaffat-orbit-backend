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


class CreateAttendance(BaseCRUDView, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'generic/form.html'
    create = True
    success_url = reverse_lazy('attendance:attendance_list')
    view_name = "Create Attendance"


class UpdateAttendance(BaseCRUDView, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    success_url = reverse_lazy('attendance:attendance_list')
    view_name = "Update Attendance"


class DeleteAttendance(BaseDeleteView):
    model = Attendance
    view_name = "Delete Attendance"


#API Views
class CheckinAPI_V1(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return api_response(
                errorno=1,
                message="خطأ في التحقق من البيانات.",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        result = AttendanceService.checkin(
            user=request.user,
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
        )

        if result["status"] == "out_of_range":
            return api_response(
                errorno=2,
                message=result["message"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if result["status"] == "already_checked_in":
            return api_response(
                errorno=3,
                message=result["message"],
                status_code=status.HTTP_200_OK,
            )

        if result["status"] == "weekend":
            return api_response(
                errorno=4,
                message=result["message"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        
        return api_response(
            errorno=0,
            message=result["message"],
            status_code=status.HTTP_200_OK,
        )



class CheckoutAPI_V1(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return api_response(
                errorno=1,
                message="خطأ في التحقق من البيانات.",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        result = AttendanceService.checkout(
            user=request.user,
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
        )

        if result["status"] == "out_of_range":
            return api_response(
                errorno=2,
                message=result["message"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if result["status"] == "no_checkin":
            return api_response(
                errorno=3,
                message=result["message"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if result["status"] == "already_checked_out":
            return api_response(
                errorno=4,
                message=result["message"],
                status_code=status.HTTP_200_OK,
            )

        if result["status"] == "weekend":
            return api_response(
                errorno=5,
                message=result["message"],
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        
        return api_response(
            errorno=0,
            message=result["message"],
            status_code=status.HTTP_200_OK,
        )