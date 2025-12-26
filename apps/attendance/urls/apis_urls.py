from django.urls import path

from ..views import apis_views



urlpatterns = [
    
    path('api/v1/checkin/', apis_views.CheckinAPI_V1.as_view(), name='attendance_checkin_api_v1'),
    path('api/v1/checkout/', apis_views.CheckoutAPI_V1.as_view(), name='attendance_checkout_api_v1'),
    
]