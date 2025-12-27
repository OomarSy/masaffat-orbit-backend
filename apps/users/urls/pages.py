from django.urls import path

from ..views import pages_views

app_name = "users"

urlpatterns = [
    
    # User Management Paths
    path('list', pages_views.ListUser.as_view(), name='user_list'),
    path('create/', pages_views.CreateUser.as_view(), name='user_create'),
    path('<int:pk>/', pages_views.DetailsUser.as_view(), name='user_detail'),
    path('<int:pk>/edit/', pages_views.UpdateUser.as_view(), name='user_update'),
    path('<int:pk>/delete/', pages_views.DeleteUser.as_view(), name='user_delete'),
    
    #Auth Pages
    path('accounts/login/', pages_views.UserLoginView.as_view(), name="login"),
    path('accounts/logout/', pages_views.logout_view, name="logout"),

]
