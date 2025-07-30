from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from  apps.wallet.services.bitcoinrpc import BitcoinRPC
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Génération d’une adresse Bitcoin via Bitcoin Core RPC
            try:
                client = BitcoinRPC()
                address = client.rpc.getnewaddress()
                user.bitcoin_address = address
                user.save()
            except Exception as e:
                return Response(
                    {'error': f"Erreur RPC : {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                'user': UserSerializer(user).data,
                'access': access_token,
                'refresh': str(refresh),
                'message': 'Inscription réussie.'
            }, status=status.HTTP_201_CREATED)

            # Cookie HTTP Only pour le token
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=3600
            )

            # Stocker l’ID utilisateur dans la session Django
            request.session['user_id'] = user.id
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Nom d’utilisateur et mot de passe requis'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'},
                            status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Mot de passe incorrect'},
                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({
            'user': UserSerializer(user).data,
            'access': access_token,
            'refresh': str(refresh),
            'message': 'Connexion réussie.'
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=3600
        )

        request.session['user_id'] = user.id
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        request.session.flush()
        return response


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serialized = UserSerializer(user)
        return Response(serialized.data, status=status.HTTP_200_OK)
