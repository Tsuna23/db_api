from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from Backend.models import Utilisateur


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        if login and password:
            user = authenticate(
                request=self.context.get('request'),
                username=login,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    'Identifiants invalides',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'Ce compte est désactivé',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Le login et le mot de passe sont requis',
                code='authorization'
            )

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                'L\'ancien mot de passe est incorrect'
            )
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Les mots de passe ne correspondent pas'
            })
        
        # Valider le nouveau mot de passe selon les règles Django
        validate_password(attrs['new_password'], self.context['request'].user)
        
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            'id',
            'login',
            'nom',
            'prenom',
            'role',
            'photo',
            'is_active'
        ]
        read_only_fields = ['id', 'role']