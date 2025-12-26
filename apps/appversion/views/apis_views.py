from rest_framework.views import APIView
from rest_framework import status

from packaging.version import Version, InvalidVersion

from ..services.AppUpdateService import AppUpdateService
from apps.core.utils import api_response


class AppUpdateCheckAPI_V1(APIView):

    def get(self, request):
        current_version = request.GET.get("current_version")

        if not current_version:
            return api_response(
                errorno=1,
                message="'current_version' parameter is missing.",
                data={},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            Version(current_version)
        except InvalidVersion:
            return api_response(
                errorno=2,
                message="'current_version' format is invalid.",
                data={},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            update_info = AppUpdateService.check_update(current_version, request=request)
        except Exception as e:
            return api_response(
                errorno=99,
                message="An error occurred while checking for updates.",
                data={},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        msg_map = {
            "force": "UPDATE_REQUIRED",
            "optional": "UPDATE_AVAILABLE",
            "none": "UP_TO_DATE"
        }
        update_type = update_info.get("update_type", "none")

        return api_response(
            errorno=0,
            message=msg_map.get(update_type, "UP_TO_DATE"),
            data=update_info,
            status_code=status.HTTP_200_OK
        )