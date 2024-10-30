# accounts/urls.py
from django.urls import path
from django.views.generic import RedirectView

from .views import SignupView, LoginView, UserListView, UserDetailView  # Corrigido para UserDetailView

urlpatterns = [
    path('', RedirectView.as_view(url='/home/'), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
