from django.urls import path

from ..views import pages_views


urlpatterns = [
    
    path('', pages_views.dashboard, name="index"),

]