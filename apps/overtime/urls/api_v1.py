from django.urls import path
from ..views import apis_views as views

app_name = "overtime-api-v1"

urlpatterns = [
    path('create/', views.OvertimeCreateAPI_V1.as_view(), name='overtime_create_api_v1'),
    path('list/', views.OvertimeListAPI_v1.as_view(), name='overtime_list_api_v1'),
]