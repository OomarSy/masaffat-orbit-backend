from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from apps.attendance.filters import AttendanceFilter, OvertimeFilter
from .tables import AttendanceTable, OvertimeTable
from .service.attendance import AttendanceService
from .serializers import OvertimeEntrySerializer
from .forms import AttendanceForm, OvertimeForm
from .models import Attendance, Overtime

from .service.attendance import OvertimeService
from .serializers import AttendanceSerializer

from base.views import BaseCRUDView, BaseDeleteView, BaseListView
from base.utils import api_response

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


# Overtime Views
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


class OvertimeAPI_V1(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        entries = request.data.get("entries", [])
        if not isinstance(entries, list) or not entries:
            return api_response(
                errorno=1,
                message="يرجى تمرير قائمة صحيحة من الإدخالات.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = OvertimeEntrySerializer(data=entries, many=True)
        if not serializer.is_valid():
            return api_response(
                errorno=2,
                message="خطأ في التحقق من البيانات.",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        created, errors = OvertimeService.create_overtime(request.user, serializer.validated_data)

        return api_response(
            errorno=0,
            message="تمت معالجة الدوام الإضافي.",
            data={
                "created": created,
                "errors": errors
            },
            status_code=status.HTTP_200_OK
        )


class OvertimeAPI_V1(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        entries = request.data.get("entries", [])
        if not isinstance(entries, list) or not entries:
            return api_response(
                errorno=1,
                message="يرجى تمرير قائمة صحيحة من الإدخالات.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = OvertimeEntrySerializer(data=entries, many=True)
        if not serializer.is_valid():
            return api_response(
                errorno=2,
                message="خطأ في التحقق من البيانات.",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        created, errors = OvertimeService.create_overtime(request.user, serializer.validated_data)

        return api_response(
            errorno=0,
            message="تمت معالجة الدوام الإضافي.",
            data={
                "created": created,
                "errors": errors
            },
            status_code=status.HTTP_200_OK
        )