from django.urls import path

from apps.attendance import views



urlpatterns = [
    
    # Attendance Paths
    path('attendance/list', views.ListAttendance.as_view(), name='attendance_list'),
    path('attendance/details/<int:pk>', views.DetailsAttendance.as_view(), name='attendance_detail'),
    path('attendance/create/', views.CreateAttendance.as_view(), name='attendance_create'),
    path('attendance/update/<int:pk>', views.UpdateAttendance.as_view(), name='attendance_update'),
    path('attendance/delete/<int:pk>', views.DeleteAttendance.as_view(), name='attendance_delete'),   

    # Overtime Paths
    path('overtime/list', views.ListOvertime.as_view(), name='overtime_list'),
    path('overtime/details/<int:pk>', views.DetailsOvertime.as_view(), name='overtime_detail'),
    path('overtime/create/', views.CreateOvertime.as_view(), name='overtime_create'),
    path('overtime/update/<int:pk>', views.UpdateOvertime.as_view(), name='overtime_update'),
    path('overtime/delete/<int:pk>', views.DeleteOvertime.as_view(), name='overtime_delete'),
    
    # API Paths
    path('api/v1/checkin/', views.CheckinAPI_V1.as_view(), name='attendance_checkin_api_v1'),
    path('api/v1/checkout/', views.CheckoutAPI_V1.as_view(), name='attendance_checkout_api_v1'),
    path('api/v1/overtime/', views.OvertimeAPI_V1.as_view(), name='overtime_api_v1'),
    
]