from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Role(models.TextChoices):
    ADMINISTRATEUR = 'Administrateur', _('Administrateur')
    # Aucun autre rôle pour l'instant


class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('Le champ login est obligatoire.')
        
        # Vérifier qu'il n'y a pas déjà un administrateur
        if Utilisateur.objects.filter(role=Role.ADMINISTRATEUR).exists():
            raise ValueError('Un administrateur existe déjà')
        
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        # Vérifier qu'il n'y a pas déjà un administrateur
        if Utilisateur.objects.filter(role=Role.ADMINISTRATEUR).exists():
            raise ValueError('Un administrateur existe déjà')
        
        extra_fields.setdefault('role', Role.ADMINISTRATEUR)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(login, password, **extra_fields)


class Utilisateur(AbstractUser):
    username = None
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    login = models.CharField(max_length=100, unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ADMINISTRATEUR
    )
    
    photo = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True) 
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['nom', 'prenom']
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(role=Role.ADMINISTRATEUR),
                name='single_admin_role'
            )
        ]
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def is_administrateur(self):
        return self.role == Role.ADMINISTRATEUR
    
    def save(self, *args, **kwargs):
        # S'assurer qu'on ne peut créer qu'un seul administrateur
        if self._state.adding and Utilisateur.objects.filter(role=Role.ADMINISTRATEUR).exists():
            raise ValidationError("Un seul administrateur est autorisé")
        
        # Toujours définir comme superuser pour les permissions
        self.is_superuser = True
        super().save(*args, **kwargs)