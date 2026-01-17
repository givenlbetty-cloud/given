from django.db import models
from django.conf import settings
from formations.models import Programme

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('completed', 'Terminé'),
        ('failed', 'Échoué'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_id = models.CharField(max_length=100, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Paiement {self.id} - {self.user} - {self.montant}€"
