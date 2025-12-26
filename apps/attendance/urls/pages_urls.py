from django.urls import path

from ..views import pages_views


urlpatterns = [
    
    # Attendance Paths
    path('attendance/list', pages_views.ListAttendance.as_view(), name='attendance_list'),
    path('attendance/details/<int:pk>', pages_views.DetailsAttendance.as_view(), name='attendance_detail'),
    path('attendance/create/', pages_views.CreateAttendance.as_view(), name='attendance_create'),
    path('attendance/update/<int:pk>', pages_views.UpdateAttendance.as_view(), name='attendance_update'),
    path('attendance/delete/<int:pk>', pages_views.DeleteAttendance.as_view(), name='attendance_delete'),   
    
]