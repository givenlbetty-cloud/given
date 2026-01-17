import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
django.setup()

from accounts.models import CustomUser

def create_superuser():
    username = 'admin'
    email = 'admin@atj.com'
    password = 'admin123'

    if not CustomUser.objects.filter(username=username).exists():
        print(f"Création du superuser : {username}")
        CustomUser.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Superuser '{username}' créé avec succès (Mot de passe: {password}).")
    else:
        print(f"Information : Le superuser '{username}' existe déjà.")

if __name__ == "__main__":
    create_superuser()

if __name__ == '__main__':
    create_superuser()
