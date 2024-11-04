from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')  # Ajuste para o nome da URL de signup
        self.login_url = reverse('login')     # Ajuste para o nome da URL de login
        self.user_data = {
            'first_name': 'Test User',
            'email': 'test@example.com',
            'password': 'strongpassword',
            'password_confirm': 'strongpassword'
        }
        self.user = User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            fist_name=self.user_data['name']
        )

    def test_signup(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # 1 user already exists in setUp
        self.assertEqual(User.objects.get(email='test@example.com').name, 'Test User')

    def test_signup_password_mismatch(self):
        invalid_data = self.user_data.copy()
        invalid_data['password_confirm'] = 'differentpassword'
        response = self.client.post(self.signup_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Supondo que você retorne um token ao fazer login

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crud_user(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.user_data['name'])

        # Update user
        response = self.client.patch(reverse('user-detail', kwargs={'pk': self.user.id}), {'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated Name')

        # Delete user
        response = self.client.delete(reverse('user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)  # Verifica se o usuário foi deletado

    def test_access_crud_without_login(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Verifica acesso negado
