from django.urls import path

from ..views import apis_views

app_name = "appversion-api-v1"

urlpatterns = [

    path('app/update-check/', apis_views.AppUpdateCheckAPI_V1.as_view(), name='app_update_check_api_v1'),

]
