import os
import django
import sys
from getpass import getpass

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ANG_AVI.settings')
django.setup()

from Backend.models.auth_user_model import Utilisateur, Role

def create_admin_auto():
    """Création automatique depuis variables d'environnement (pour production)"""
    login = os.environ.get('ADMIN_LOGIN')
    password = os.environ.get('ADMIN_PASSWORD')
    nom = os.environ.get('ADMIN_NOM', 'Admin')
    prenom = os.environ.get('ADMIN_PRENOM', 'Super')
    
    if not login or not password:
        print("⚠️ Mode auto : ADMIN_LOGIN et ADMIN_PASSWORD non définis")
        return False
    
    if Utilisateur.objects.filter(login=login).exists():
        print(f"✅ Admin {login} existe déjà")
        return True
    
    try:
        admin = Utilisateur.objects.create_superuser(
            login=login,
            password=password,
            nom=nom,
            prenom=prenom,
            role=Role.ADMINISTRATEUR
        )
        print(f"✅ Admin créé : {login}")
        return True
    except Exception as e:
        print(f"❌ Erreur création admin : {e}")
        return False

def create_admin_securise():
    """Création interactive (pour développement local)"""
    print("CRÉATION SÉCURISÉE DE L'ADMINISTRATEUR")
    print("=" * 50)
    
    if Utilisateur.objects.filter(role=Role.ADMINISTRATEUR).exists():
        print("Un administrateur existe déjà.")
        sys.exit(1)
    
    print("\nVeuillez saisir les informations :")
    
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    login = input("Login : ").strip()
    
    print("\nSAISIE DU MOT DE PASSE :")
    print("(Le mot de passe ne s'affichera pas à l'écran)")
    
    while True:
        password = getpass("Mot de passe : ")
        confirm = getpass("Confirmer le mot de passe : ")
        
        if password != confirm:
            print("Les mots de passe ne correspondent pas.")
            continue
        
        if len(password) < 12:
            print("Minimum 12 caractères.")
            continue
        
        if not any(c.isupper() for c in password):
            print("Doit contenir une majuscule.")
            continue
            
        if not any(c.isdigit() for c in password):
            print("Doit contenir un chiffre.")
            continue
            
        break
    
    print(f"\nNom : {nom}")
    print(f"Prénom : {prenom}")
    print(f"Login : {login}")
    print(f"Longueur mot de passe : {len(password)} caractères")

    confirm = input("\nCréer l'administrateur ? (o/n) : ").lower()
    
    if confirm != 'o':
        print("Annulé.")
        sys.exit(0)
    
    try:
        admin = Utilisateur.objects.create_superuser(
            login=login,
            password=password,
            nom=nom,
            prenom=prenom,
            role=Role.ADMINISTRATEUR
        )
        
        print("\n✅ ADMINISTRATEUR CRÉÉ !")
        print("=" * 50)
        print(f"Login : {login}")
        print(f"Nom complet : {prenom} {nom}")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    # Essayer d'abord le mode auto, sinon mode interactif
    if not create_admin_auto():
        create_admin_securise()