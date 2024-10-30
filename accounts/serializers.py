from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fieldsets = ['id', 'email', 'nome', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            nome=validated_data['nome'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user