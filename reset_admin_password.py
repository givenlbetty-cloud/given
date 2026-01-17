import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
django.setup()

from accounts.models import CustomUser

def reset_password():
    username = 'admin'
    new_password = 'admin123'

    try:
        user = CustomUser.objects.get(username=username)
        user.set_password(new_password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"✅ Succès : Le mot de passe pour '{username}' a été réinitialisé à '{new_password}'.")
    except CustomUser.DoesNotExist:
        print(f"⚠️  Attention : L'utilisateur '{username}' n'existe pas. Création en cours...")
        CustomUser.objects.create_superuser(username, 'admin@example.com', new_password)
        print(f"✅ Succès : Superuser '{username}' créé avec le mot de passe '{new_password}'.")

if __name__ == "__main__":
    reset_password()

if __name__ == '__main__':
    reset_password()
