from django.urls import path

from ..views import apis_views

app_name = "attendance-api-v1"

urlpatterns = [
    
    path('checkin/', apis_views.CheckinAPI_V1.as_view(), name='checkin_api_v1'),
    path('checkout/', apis_views.CheckoutAPI_V1.as_view(), name='checkout_api_v1'),
    
]