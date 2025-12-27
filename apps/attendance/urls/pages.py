from django.urls import path

from ..views import pages_views

app_name = "attendance"

urlpatterns = [
    
    # Attendance Paths
    path('list', pages_views.ListAttendance.as_view(), name='attendance_list'),
    path('details/<int:pk>', pages_views.DetailsAttendance.as_view(), name='attendance_detail'),
    path('create/', pages_views.CreateAttendance.as_view(), name='attendance_create'),
    path('update/<int:pk>', pages_views.UpdateAttendance.as_view(), name='attendance_update'),
    path('delete/<int:pk>', pages_views.DeleteAttendance.as_view(), name='attendance_delete'),   
]