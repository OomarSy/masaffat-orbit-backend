from django.urls import path

from ..views import pages_views

app_name = "attendance"

urlpatterns = [
    
    # Employee Attendance Paths
    path('list', pages_views.ListEmployeeAttendance.as_view(), name='employeeattendance_list'),
    path('details/<int:pk>', pages_views.DetailsEmployeeAttendance.as_view(), name='employeeattendance_detail'),
    path('create/', pages_views.CreateEmployeeAttendance.as_view(), name='employeeattendance_create'),
    path('update/<int:pk>', pages_views.UpdateEmployeeAttendance.as_view(), name='employeeattendance_update'),
    path('delete/<int:pk>', pages_views.DeleteEmployeeAttendance.as_view(), name='employeeattendance_delete'),   
]