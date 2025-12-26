from django.urls import path

from ..views import apis_views



urlpatterns = [
    
    path('api/v1/overtime/', apis_views.OvertimeAPI_V1.as_view(), name='overtime_api_v1'),
    path('api/v1/overtime/list/', apis_views.UserOvertimeListAPI_v1.as_view(), name='overtime_approve_api_v1'),
    
]