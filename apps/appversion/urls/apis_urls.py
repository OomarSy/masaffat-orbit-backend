from django.urls import path

from ..views import apis_views


urlpatterns = [

    path('api/v1/app/version/check/', apis_views.AppUpdateCheckAPI_V1.as_view(), name='app_update_check_api_v1'),

]
