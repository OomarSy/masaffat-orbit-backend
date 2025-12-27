from django.urls import path
from ..views import pages_views as views

app_name = "overtime"

urlpatterns = [
    path('list', views.ListOvertime.as_view(), name='overtime_list'),
    path('create/', views.CreateOvertime.as_view(), name='overtime_create'),
    path('<int:pk>/', views.DetailsOvertime.as_view(), name='overtime_detail'),
    path('<int:pk>/update/', views.UpdateOvertime.as_view(), name='overtime_update'),
    path('<int:pk>/delete/', views.DeleteOvertime.as_view(), name='overtime_delete'),
]
