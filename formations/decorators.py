from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Session, Inscription

def payment_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # On s'assure que l'utilisateur est connecté (redondance sécurité)
        if not request.user.is_authenticated:
            messages.warning(request, "Veuillez vous connecter pour accéder à ce contenu.")
            return redirect('login')

        session_id = kwargs.get('session_id')
        session = get_object_or_404(Session, id=session_id)
        
        # Vérification 1 : L'inscription existe-t-elle ?
        try:
            inscription = Inscription.objects.get(user=request.user, session=session)
        except Inscription.DoesNotExist:
             messages.warning(request, "Vous n'êtes pas inscrit à cette session.")
             return redirect('programmes') 
        
        # Vérification 2 : Le paiement est-il validé ?
        if inscription.statut_paiement != 'paid':
            messages.error(request, "⛔ Ce contenu est réservé aux membres inscrits. Veuillez finaliser votre paiement.")
            return redirect('accounts:simuler_paiement', inscription_id=inscription.id)
            
        # Si tout est OK, on passe la main à la vue
        # On peut injecter l'inscription dans la requête pour éviter une requete DB en plus dans la vue
        request.inscription = inscription
        return view_func(request, *args, **kwargs)
    return _wrapped_view
