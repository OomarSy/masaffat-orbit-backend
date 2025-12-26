from django.urls import path

from ..views import pages_views


urlpatterns = [

    # Overtime Paths
    path('overtime/list', pages_views.ListOvertime.as_view(), name='overtime_list'),
    path('overtime/details/<int:pk>', pages_views.DetailsOvertime.as_view(), name='overtime_detail'),
    path('overtime/create/', pages_views.CreateOvertime.as_view(), name='overtime_create'),
    path('overtime/update/<int:pk>', pages_views.UpdateOvertime.as_view(), name='overtime_update'),
    path('overtime/delete/<int:pk>', pages_views.DeleteOvertime.as_view(), name='overtime_delete'),
    
]