from django.urls import path

from ..views import pages_views

app_name = "dashboard"

urlpatterns = [
    
    path('', pages_views.dashboard, name="index"),

]