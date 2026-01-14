from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Programme, Session, Inscription
from django.contrib import messages

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
            messages.success(request, f"Inscription à {session.programme.titre} effectuée. Veuillez procéder au paiement.")
        return redirect('accounts:dashboard')
    return redirect('programmes')
