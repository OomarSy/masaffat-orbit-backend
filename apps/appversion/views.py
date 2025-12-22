from rest_framework.views import APIView
from rest_framework import status
from packaging.version import Version, InvalidVersion
from django.views.generic import DetailView, CreateView, UpdateView
from apps.appversion.filters import AppVersionFilter
from apps.appversion.forms import AppVersionForm
from apps.appversion.models import AppVersion
from apps.appversion.services.AppUpdateService import AppUpdateService
from apps.appversion.tables import AppVersionTable
from base.utils import api_response
from django.urls import reverse_lazy
from base.views import BaseCRUDView, BaseDeleteView, BaseListView

# AppVersion Views
class ListAppVersion(BaseListView):
    model = AppVersion
    table_class = AppVersionTable
    filterset_class = AppVersionFilter
    view_name = "AppVersion"
    add_url_name = 'appversion:appversion_create'
    segment = "appversion"


class DetailsAppVersion(BaseCRUDView, DetailView):
    model = AppVersion
    form_class = AppVersionForm
    view_name = "AppVersion Details"
    details = True
    segment = "appversion"


class CreateAppVersion(BaseCRUDView, CreateView):
    model = AppVersion
    form_class = AppVersionForm
    template_name = 'generic/form.html'
    create = True
    success_url = reverse_lazy('appversion:appversion_list')
    view_name = "Create AppVersion"
    segment = "appversion"

class UpdateAppVersion(BaseCRUDView, UpdateView):
    model = AppVersion
    form_class = AppVersionForm
    success_url = reverse_lazy('appversion:appversion_list')
    view_name = "Update AppVersion"
    segment = "appversion"


class DeleteAppVersion(BaseDeleteView):
    model = AppVersion
    view_name = "Delete AppVersion"
    segment = "appversion"


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