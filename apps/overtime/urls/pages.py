from django.urls import path
from ..views import pages_views as views

app_name = "overtime"

urlpatterns = [
    path('list', views.ListEmployeeOvertime.as_view(), name='employeeovertime_list'),
    path('create/', views.CreateEmployeeOvertime.as_view(), name='employeeovertime_create'),
    path('<int:pk>/', views.DetailsEmployeeOvertime.as_view(), name='employeeovertime_detail'),
    path('<int:pk>/update/', views.UpdateEmployeeOvertime.as_view(), name='employeeovertime_update'),
    path('<int:pk>/delete/', views.DeleteEmployeeOvertime.as_view(), name='employeeovertime_delete'),
]
