from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.utils import timezone

from apps.location.serializers import UserLocationCMSSerializer, UserLocationSerializer
from apps.location.service.location import UserLocationService

from base.utils import api_response


class CMSUserLocationsAPI_V1(APIView):
    """
    Return all users with their coordinates for displaying on the CMS map.
    Only accessible by admin/staff users.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        locations = UserLocationService.get_all_user_locations()
        serializer = UserLocationCMSSerializer(locations, many=True)

        return api_response(
            errorno=0,
            message="User locations fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class UserLocationsPageView(UserPassesTestMixin, TemplateView):
    template_name = "pages/location/map.html"
    segment = "location"
    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Dashboard', 'url': '/dashboard/'},
            {'name': 'Locations', 'url': ''},
        ]
        context['unread_notifications_count'] = 0
        context['segment'] = self.segment
        return context


class UpdateLocationAPI_V1(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLocationSerializer

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
            location = UserLocationService.update_user_location(
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
