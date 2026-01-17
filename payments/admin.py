from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'programme', 'montant', 'date_creation', 'status')
    list_filter = ('status', 'date_creation')
    search_fields = ('user__username', 'stripe_id')

