import os
import django
import sys
from getpass import getpass

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ANG_AVI.settings')
django.setup()

from Backend.models.auth_user_model import Utilisateur, Role

def create_admin_securise():
    print("CRÉATION SÉCURISÉE DE L'ADMINISTRATEUR")
    print("=" * 50)
    
    # Vérifier si admin existe déjà
    if Utilisateur.objects.filter(role=Role.ADMINISTRATEUR).exists():
        print("Un administrateur existe déjà.")
        sys.exit(1)
    
    # Demander les infos de manière sécurisée
    print("\nVeuillez saisir les informations :")
    
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    login = input("Login : ").strip()
    
    # Saisie sécurisée du mot de passe (ne s'affiche pas)
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
        
        # Validation basique
        if not any(c.isupper() for c in password):
            print("Doit contenir une majuscule.")
            continue
            
        if not any(c.isdigit() for c in password):
            print("Doit contenir un chiffre.")
            continue
            
        break
    
    # Confirmation
    print(f"\nNom : {nom}")
    print(f"Prénom : {prenom}")
    print(f"Login : {login}")
    print(f"Longueur mot de passe : {len(password)} caractères")

    confirm = input("\nCréer l'administrateur ? (o/n) : ").lower()
    
    if confirm != 'o':
        print("Annulé.")
        sys.exit(0)
    
    try:
        # Création
        admin = Utilisateur.objects.create_superuser(
            login=login,
            password=password,
            nom=nom,
            prenom=prenom,
            role=Role.ADMINISTRATEUR
        )
        
        print("\n ADMINISTRATEUR CRÉÉ !")
        print("=" * 50)
        print(f"Login : {login}")
        print(f"Nom complet : {prenom} {nom}")
        print("\n IMPORTANT :")
        print("1. Notez le mot de passe dans un gestionnaire sécurisé")
        print("2. Changez-le après première connexion")
        print("3. Ces informations ne seront plus affichées")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    create_admin_securise()