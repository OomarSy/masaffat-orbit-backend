from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.attendance.serializers import OvertimeEntrySerializer
from apps.attendance.service.attendance import OvertimeService
from apps.attendance.serializers import AttendanceSerializer
from apps.attendance.service.attendance import AttendanceService
from base.utils import api_response

class CheckinAPI_V1(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return api_response(
                errorno=1,
                message="Validation error.",
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
                message="Validation error.",
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