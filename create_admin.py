import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
django.setup()

from accounts.models import CustomUser

def create_superuser():
    username = 'admin'
    email = 'admin@atj.com'
    password = 'admin'

    if not CustomUser.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        CustomUser.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")

if __name__ == '__main__':
    create_superuser()
