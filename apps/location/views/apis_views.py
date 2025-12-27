from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework import status

from django.utils.dateparse import parse_datetime
from django.utils import timezone

from apps.location.models import EmployLocationHistory

from ..utils import parse_query_datetime
from ..serializers import EmployLocationCMSSerializer, EmployLocationSerializer
from ..services.location import EmployLocationService

from apps.core.utils import api_response


class EmployLocationsAPI_V1(APIView):
    """
    Return all users with their coordinates for displaying on the CMS map.
    Only accessible by admin/staff users.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        locations = EmployLocationService.get_all_user_locations()
        serializer = EmployLocationCMSSerializer(locations, many=True)

        return api_response(
            errorno=0,
            message="User locations fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class CMSEmployLocationsHistoryAPI_V1(APIView):
    """
    Return user locations history filtered by date range.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        user_id = request.GET.get('user_id')
        start_date = request.GET.get('start_date')  # ISO format
        end_date = request.GET.get('end_date')

        qs = EmployLocationHistory.objects.all()
        if user_id:
            qs = qs.filter(user_id=user_id)
        if start_date:
            qs = qs.filter(recorded_at__gte=parse_datetime(start_date))
        if end_date:
            qs = qs.filter(recorded_at__lte=parse_datetime(end_date))

        data = [
            {
                'user_id': loc.user.id,
                'username': loc.user.username,
                'latitude': float(loc.latitude),
                'longitude': float(loc.longitude),
                'recorded_at': loc.recorded_at.isoformat(),
            }
            for loc in qs
        ]

        return api_response(
            errorno=0,
            message="User location history fetched successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )


class UpdateLocationAPI_V1(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployLocationSerializer

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

        try:
            location = EmployLocationService.update_user_location(
                user=request.user,
                latitude=data["latitude"],
                longitude=data["longitude"],
            )
        except Exception as e:
            return api_response(
                errorno=2,
                message="لم يتم تحديث الموقع بسبب خطأ داخلي.",
                data={"detail": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return api_response(
            errorno=0,
            message="تم تحديث الموقع بنجاح.",
            data={
                "latitude": str(location.latitude),
                "longitude": str(location.longitude),
                "updated_at": timezone.localtime(location.updated_at).isoformat()
            },
            status_code=status.HTTP_200_OK
        )


class EmployeeLocationHistoryAPI_V1(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user_id = request.GET.get("user_id")
        from_date = parse_query_datetime(request.GET.get("start_date"))
        to_date = parse_query_datetime(request.GET.get("end_date"))

        qs = EmployLocationHistory.objects.all()
        if user_id:
            qs = qs.filter(user_id=user_id)
        if from_date:
            qs = qs.filter(recorded_at__gte=from_date)
        if to_date:
            qs = qs.filter(recorded_at__lte=to_date)

        data = [
            {
                "user_id": loc.user.id,
                "username": loc.user.username,
                "latitude": float(loc.latitude),
                "longitude": float(loc.longitude),
                "recorded_at": loc.recorded_at.isoformat(),
            }
            for loc in qs
        ]

        return api_response(
            errorno=0,
            message="تم جلب سجل المواقع بنجاح.",
            data=data
        )
