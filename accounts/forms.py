from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'photo')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'  # Force role to student
        if commit:
            user.save()
        return user
