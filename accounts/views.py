# accounts/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # Corrigido 'Login' para 'login'
from django.contrib.auth.models import User as AuthUser  # Evitando confusão com nosso User model
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, LoginSerializer  # Certifique-se de que LoginSerializer está definido


# Create your views here.

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)  # Corrigido para usar a função 'login' do Django
            # return Response({"message": "Login realizado com sucesso"}, status=status.HTTP_200_OK)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        else:
            # return Response({"error": "Credenciais inválidas"}, status=status.HTTP_400_BAD_REQUEST)
            messages.error(request, 'Email ou senha incorretos!')
            return redirect('login')

class HomePageView(TemplateView):
    template_name = 'home.html'


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Você pode ajustar as permissões conforme necessário




class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Você pode ajustar as permissões conforme necessário


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')