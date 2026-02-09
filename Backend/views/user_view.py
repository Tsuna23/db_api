from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from Backend.serializers.auth_user_serializer import (
    LoginSerializer,
    ChangePasswordSerializer,
    UtilisateurSerializer
)


def get_tokens_for_user(user):
    """Générer les tokens JWT pour un utilisateur"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    """
    Vue pour l'authentification de l'utilisateur avec JWT
    POST /auth/login/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Générer les tokens JWT
            tokens = get_tokens_for_user(user)
            
            user_serializer = UtilisateurSerializer(user)
            
            return Response({
                'message': 'Connexion réussie',
                'user': user_serializer.data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    """
    Vue pour la déconnexion de l'utilisateur (blacklist du refresh token)
    POST /auth/logout/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Déconnexion réussie'
            }, status=status.HTTP_200_OK)
        except TokenError:
            return Response({
                'error': 'Token invalide ou déjà blacklisté'
            }, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthView(APIView):
    """
    Vue pour vérifier si l'utilisateur est authentifié
    GET /auth/check/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UtilisateurSerializer(request.user)
        return Response({
            'authenticated': True,
            'user': user_serializer.data
        }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    Vue pour gérer le profil de l'utilisateur
    GET /auth/profile/ - Récupérer le profil
    PUT /auth/profile/ - Modifier complètement le profil
    PATCH /auth/profile/ - Modifier partiellement le profil
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Récupérer les informations du profil"""
        serializer = UtilisateurSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Modifier complètement le profil"""
        serializer = UtilisateurSerializer(
            request.user,
            data=request.data
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profil modifié avec succès',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request):
        """Modifier partiellement le profil"""
        serializer = UtilisateurSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profil modifié avec succès',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ChangePasswordView(APIView):
    """
    Vue pour changer le mot de passe de l'utilisateur connecté
    POST /auth/change-password/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            # Générer de nouveaux tokens après le changement de mot de passe
            tokens = get_tokens_for_user(request.user)
            
            return Response({
                'message': 'Mot de passe modifié avec succès',
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TestChangePasswordView(APIView):
    """
    Vue de test pour changer le mot de passe sans l'ancien mot de passe
    POST /auth/test-change-password/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get('new_password')
        
        if not new_password:
            return Response({
                'error': 'Le nouveau mot de passe est requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user.set_password(new_password)
        user.save()
        
        # Générer de nouveaux tokens
        tokens = get_tokens_for_user(user)
        
        return Response({
            'message': 'Mot de passe modifié avec succès (mode test)',
            'tokens': tokens
        }, status=status.HTTP_200_OK)