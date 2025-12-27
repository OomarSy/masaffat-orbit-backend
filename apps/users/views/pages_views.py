from django.views.generic import DetailView, CreateView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy

from apps.core.views.pages_views import BaseListView, BaseCRUDView, BaseDeleteView

from ..filters import UserFilter
from ..tables import UserTable
from ..forms import UserForm
from ..forms import LoginForm


User = get_user_model()


# Users Views
class ListUser(BaseListView):
    model = User
    table_class = UserTable
    filterset_class = UserFilter
    view_name = "Users"
    add_url_name = 'users:user_create'
    segment = "users"


class DetailsUser(BaseCRUDView, DetailView):
    model = User
    form_class = UserForm
    view_name = "User Details"
    details = True


class CreateUser(BaseCRUDView, CreateView):
    model = User
    form_class = UserForm
    template_name = 'generic/form.html'
    create = True
    success_url = reverse_lazy('users:user_list')
    view_name = "Create User"


class UpdateUser(BaseCRUDView, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:user_list')
    view_name = "Update User"


class DeleteUser(BaseDeleteView):
    model = User
    view_name = "Delete User"
    segment = "users"


class UserLoginView(LoginView):
  form_class = LoginForm
  template_name = 'pages/accounts/sign-in.html'

def logout_view(request):
  logout(request)
  return redirect('/users/accounts/login/')
  
def index(request):
    return render(request, 'pages/index.html')