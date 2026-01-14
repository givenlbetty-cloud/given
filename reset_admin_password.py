import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
django.setup()

from accounts.models import CustomUser

def reset_password():
    username = 'admin'
    new_password = 'admin'

    try:
        user = CustomUser.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        print(f"Password for user '{username}' has been reset to '{new_password}'.")
    except CustomUser.DoesNotExist:
        print(f"User '{username}' does not exist.")

if __name__ == '__main__':
    reset_password()
