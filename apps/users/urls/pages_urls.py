from django.urls import path

from ..views import pages_views


urlpatterns = [
    
    # User Management Paths
    path('users/', pages_views.ListUser.as_view(), name='user_list'),
    path('users/create/', pages_views.CreateUser.as_view(), name='user_create'),
    path('users/<int:pk>/', pages_views.DetailsUser.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', pages_views.UpdateUser.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', pages_views.DeleteUser.as_view(), name='user_delete'),

    #Auth Pages
    path('accounts/login/', pages_views.UserLoginView.as_view(), name="login"),
    path('accounts/logout/', pages_views.logout_view, name="logout"),

]
