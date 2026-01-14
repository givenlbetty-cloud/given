from django.db import models
from django.conf import settings

class Mentor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField()
    expertise = models.CharField(max_length=255)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
