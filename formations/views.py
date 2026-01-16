from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Programme, Session, Inscription
from django.contrib import messages
from .decorators import payment_required

def liste_programmes(request):
    query = request.GET.get('q')
    if query:
        programmes = Programme.objects.filter(titre__icontains=query)
    else:
        programmes = Programme.objects.all()
    return render(request, 'formations/liste.html', {'programmes': programmes, 'query': query})

@login_required
def inscrire_session(request, session_id):
    if request.method == 'POST':
        session = get_object_or_404(Session, id=session_id)
        # Check if already enrolled
        if Inscription.objects.filter(user=request.user, session=session).exists():
             messages.warning(request, "Vous êtes déjà inscrit à cette session.")
        else:
            Inscription.objects.create(user=request.user, session=session)
            messages.success(request, f"Inscription à {session.programme.titre} effectuée. Veuillez procéder au paiement pour accéder au contenu.")
        return redirect('accounts:dashboard')
    return redirect('programmes')

@login_required
@payment_required
def detail_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    # L'objet inscription est déjà récupéré et vérifié par le décorateur @payment_required
    # Il est disponible via request.inscription
    inscription = getattr(request, 'inscription', None)
    
    if not inscription:
        # Fallback de sécurité au cas où le décorateur serait mal utilisé
        inscription = get_object_or_404(Inscription, user=request.user, session=session)

    return render(request, 'formations/detail_session.html', {
        'session': session,
        'inscription': inscription
    })
