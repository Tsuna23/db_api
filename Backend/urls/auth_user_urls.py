from django.urls import path
from rest_framework.authtoken import views as auth_views
from Backend.views.user_view import *
urlpatterns = [
    # 1. Authentification
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    # 2. Vérification d'authentification
    path('auth/check/', CheckAuthView.as_view(), name='check_auth'),
    
    # 3. Gestion du profil
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/test-change-password/', TestChangePasswordView.as_view(), name='test_change_password'),
]