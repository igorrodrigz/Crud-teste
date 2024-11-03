from django.urls import path
from .views import SignupView, LoginView, UserListView, UserDetailView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users-list/', UserListView.as_view(), name='users-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
