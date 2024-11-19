# accounts/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # Corrigido 'Login' para 'login'
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User as AuthUser  # Evitando confusão com nosso User model
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
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
            messages.success(request, "Usuário cadastrado com sucesso.")
            return redirect('login')
        messages.error(request, "Erro ao cadastrar usuário")
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
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha incorretos!')
            return redirect('login')

class HomePageView(LoginRequiredMixin, TemplateView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    template_name = 'home.html'

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Ajustar as permissões conforme necessário
    template_name = 'users-list.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')  # Captura o termo de busca
        users = self.get_queryset()

        if query:
            users = users.filter(first_name__icontains=query) | users.filter(email__icontains=query)

        paginator = Paginator(users, 10)  # Pagina com 10 usuários por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'page_obj': page_obj, 'query': query})

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_superuser or obj == self.request.user:
            return obj
        messages.error(self.request, 'Você não tem permissão para acessar esse usuário.')
        return HttpResponseRedirect(self.request.META.get('_REFERER', '/'))

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if isinstance(user, HttpResponseRedirect):
            return user
        return render(request, 'user-detail.html', {'user': user})

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if isinstance(user, HttpResponseRedirect):
            return user
        serializer = self.get_serializer(user, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect("user-detail", pk=user.pk)
        messages.error(request, 'Erro ao atualizar usuário')
        return redirect("user-detail", pk=user.pk)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        if isinstance(user, HttpResponseRedirect):
            return user
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if isinstance(user, HttpResponseRedirect):
            return user
        try:
            user.delete()
            messages.success(request, 'Usuário deletado com sucesso!')
            return redirect('users-list')
        except Exception as e:
            messages.error(request, f'Erro ao deletar o usuário: {str(e)}')
            return redirect('user-detail', pk=user.id)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
            return self.delete(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
