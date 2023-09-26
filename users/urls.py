from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users.views import RegisterUser, ProfileUser, ListUsersView, confirm_code, DeleteUserView, BlockUser
app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('users/login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('list_users/', ListUsersView.as_view(), name='list_users'),
    path('confirm_code/<str:email>/', confirm_code, name='confirm_code'),
    path('delete/<int:pk>/', DeleteUserView.as_view(), name='delete'),
    path('profile/', cache_page(60)(ProfileUser.as_view()), name='profile'),
    path('blocked_user/<int:pk>/', BlockUser.as_view(), name='blocked_user'),
]