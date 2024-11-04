# accounts/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # Corrigido 'Login' para 'login'
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User as AuthUser  # Evitando confusão com nosso User model
from django.core.serializers import serialize
from django.db.migrations import serializer
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
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



    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
            messages.success(request, "Usuário cadastrado com sucesso. ")
            return redirect('login')
        messages.error(request, "Erro ao cadastrar usuário")
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'signup.html', {'errors': serializer.errors})

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

class HomePageView(LoginRequiredMixin, TemplateView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    template_name = 'home.html'


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Você pode ajustar as permissões conforme necessário
    template_name = 'users-list.html'

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        return render(request, self.template_name,{'users': users})


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or obj == self.request.user:
            return obj
        # Se o usuário não tiver permissão, exibe a mensagem e redireciona para a lista de usuários
        messages.error(self.request, 'Você não tem permissão para acessar esse usuário.')
        return None

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        # Redireciona se o usuário não tiver permissão
        if not user:
            return redirect('users-list')
        return render(request, 'user-detail.html', {'user': user})

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if not user:
            return redirect('users-list')

        # Atualização dos dados do usuário
        user.first_name = request.POST.get('first_name')
        user.email = request.POST.get('email')
        user.save()

        messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect("user-detail", pk=user.pk)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        if not user:
            return redirect('users-list')

        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if not user:
            return redirect('users-list')

        try:
            user.delete()
            messages.success(request, 'Usuário deletado com sucesso!')
            return redirect('users-list')
        except Exception as e:
            messages.error(request, f'Erro ao deletar o usuário: {str(e)}')
            return redirect('user-detail', pk=user.id)

    def dispatch(self, request, *args, **kwargs):
        # Verifica o método HTTP
        if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
            return self.delete(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')