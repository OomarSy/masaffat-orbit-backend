from django.urls import path

from apps.attendance import views



urlpatterns = [
    
    path('api/v1/checkin/', views.CheckinAPI_V1.as_view(), name='attendance_checkin_api_v1'),
    path('api/v1/checkout/', views.CheckoutAPI_V1.as_view(), name='attendance_checkout_api_v1'),
    path('api/v1/overtime/', views.OvertimeAPI_V1.as_view(), name='overtime_api_v1'),
]