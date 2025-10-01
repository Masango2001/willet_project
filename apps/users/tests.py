from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch

CustomerUser = get_user_model()


class CustomerUserTests(APITestCase):

    @patch("apps.users.views.get_rpc_connection")  # On mock la fonction Bitcoin RPC
    def test_create_user_with_bitcoin_address(self, mock_rpc):
        """
        Test de création d'un utilisateur avec une adresse Bitcoin mockée.
        """
        # On configure le mock pour renvoyer une adresse factice
        mock_rpc.return_value.getnewaddress.return_value = "mocked_bitcoin_address"

        # ⚠️ Utiliser le nom exact de l'URL dans urls.py
        url = reverse("customer-create")
        data = {
            "username": "testuser",
            "password": "strongpassword123",
            "email": "test@example.com"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("crypto_address", response.data["user"])
        self.assertEqual(response.data["user"]["crypto_address"], "mocked_bitcoin_address")
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_user(self):
        """
        Test de connexion utilisateur.
        """
        # On crée un utilisateur
        user = CustomerUser.objects.create_user(
            username="testuser2",
            password="strongpassword123",
            email="test2@example.com"
        )

        url = reverse("login")
        data = {
            "username": "testuser2",
            "password": "strongpassword123"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_list_users_requires_authentication(self):
        """
        Test que la liste des utilisateurs nécessite une authentification.
        """
        url = reverse("customer-list")

        # Tentative sans token → doit échouer
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
