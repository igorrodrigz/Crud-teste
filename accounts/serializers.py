# accounts/serializers.py
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _

User = get_user_model()  # Garantindo que o User correto seja utilizado

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """Verifica se o email já está em uso"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Já existe um usuário com esse email."))
        return value

    def validate(self, data):
        """Verifica se as senhas coincidem"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError(_("As senhas não são iguais."))
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Removendo password2 antes da criação
        user = User(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
        )
        user.set_password(validated_data['password'])  # Setando a senha
        user.save()  # Salvando o usuário
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user is None:
            raise serializers.ValidationError("Credenciais inválidas.")
        data['user'] = user
        return data
