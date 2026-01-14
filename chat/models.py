from django.db import models
from django.conf import settings
from django.db.models import Q

class Thread(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='threads')
    updated_at = models.DateTimeField(auto_now=True)

    def get_messages(self):
        return self.messages.all().order_by('timestamp')

    def get_last_message(self):
        return self.messages.last()
    
    @classmethod
    def get_or_create(cls, user1, user2):
        print(f"Checking thread for {user1} and {user2}") # Debug
        # Check if a thread exists with exactly these two participants
        threads = cls.objects.filter(participants=user1).filter(participants=user2)
        if threads.exists():
            return threads.first()
        
        thread = cls.objects.create()
        thread.participants.add(user1, user2)
        return thread

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"
