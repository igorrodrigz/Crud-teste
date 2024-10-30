from django.urls import path

from CRUD.urls import urlpatterns
from .views import SignUpView, LoginView, UserListView, UserDetailUser

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailUser.as_view(), name='user-detail'),
]