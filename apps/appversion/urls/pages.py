from django.urls import path

from ..views import pages_views

app_name = "appversion"

urlpatterns = [

    # Android App Release Paths
    path('list', pages_views.ListAndroidAppRelease.as_view(), name='androidapprelease_list'),
    path('details/<int:pk>', pages_views.DetailsAndroidAppRelease.as_view(), name='androidapprelease_detail'),
    path('create/', pages_views.CreateAndroidAppRelease.as_view(), name='androidapprelease_create'),
    path('update/<int:pk>', pages_views.UpdateAndroidAppRelease.as_view(), name='androidapprelease_update'),
    path('delete/<int:pk>', pages_views.DeleteAndroidAppRelease.as_view(), name='androidapprelease_delete'),
]
