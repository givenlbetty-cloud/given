from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Formation, Session, Inscription, Lecon
from django.contrib import messages
from .decorators import payment_required


def liste_formations(request):
    query = request.GET.get('q')
    categorie = request.GET.get('categorie')
    formations = Formation.objects.filter(est_publie=True)

    if query:
        formations = formations.filter(titre__icontains=query)
    if categorie:
        formations = formations.filter(categorie=categorie)

    return render(request, 'formations/liste.html', {
        'formations': formations,
        'query': query,
        'categorie': categorie,
    })


@login_required
def inscrire_session(request, session_id):
    if request.method == 'POST':
        session = get_object_or_404(Session, id=session_id)
        inscription, created = Inscription.objects.get_or_create(
            user=request.user, session=session
        )
        if created:
            if session.formation.est_gratuit:
                inscription.statut_paiement = 'paid'
                inscription.statut_validation = True
                inscription.save()
                messages.success(request, f"Inscription confirmée pour {session.formation.titre}.")
                return redirect('formations:detail_session', session_id=session.id)
            else:
                messages.info(request, "Inscription pré-enregistrée. Veuillez procéder au paiement.")
                return redirect('formations:paiement_session', session_id=session.id)
        else:
            if inscription.statut_paiement == 'paid':
                messages.info(request, "Vous êtes déjà inscrit et à jour de paiement.")
                return redirect('formations:detail_session', session_id=session.id)
            else:
                return redirect('formations:paiement_session', session_id=session.id)

    return redirect('formations:liste')


@login_required
def paiement_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    inscription = get_object_or_404(Inscription, user=request.user, session=session)
    if inscription.statut_paiement == 'paid':
        return redirect('formations:detail_session', session_id=session.id)
    return render(request, 'formations/paiement.html', {
        'session': session,
        'formation': session.formation,
        'inscription': inscription,
    })


@login_required
def process_payment(request, session_id):
    if request.method == 'POST':
        import uuid
        from .models import Paiement
        session = get_object_or_404(Session, id=session_id)
        inscription = get_object_or_404(Inscription, user=request.user, session=session)

        inscription.statut_paiement = 'paid'
        inscription.statut_validation = True
        inscription.save()

        Paiement.objects.create(
            user=request.user,
            inscription=inscription,
            montant=session.formation.prix,
            valide=True,
            transaction_id=str(uuid.uuid4()),
        )
        messages.success(request, "Paiement accepté ! Bienvenue dans votre formation.")
        return redirect('formations:detail_session', session_id=session.id)

    return redirect('formations:paiement_session', session_id=session_id)


@login_required
@payment_required
def detail_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    inscription = getattr(request, 'inscription', None)
    if not inscription:
        inscription = get_object_or_404(Inscription, user=request.user, session=session)

    lecons = session.formation.lecons.all()
    return render(request, 'formations/detail_session.html', {
        'session': session,
        'formation': session.formation,
        'inscription': inscription,
        'lecons': lecons,
    })


@login_required
def course_content(request, session_id, lecon_id=None):
    session = get_object_or_404(Session, id=session_id)
    formation = session.formation

    inscription = Inscription.objects.filter(user=request.user, session=session).first()
    if not inscription:
        messages.warning(request, "Veuillez vous inscrire pour accéder au cours.")
        return redirect('formations:detail_session', session_id=session.id)

    if not formation.est_gratuit and inscription.statut_paiement != 'paid':
        if lecon_id:
            lecon = get_object_or_404(Lecon, id=lecon_id)
            if not lecon.est_gratuit:
                messages.warning(request, "Veuillez finaliser le paiement pour accéder à ce cours.")
                return redirect('formations:detail_session', session_id=session.id)
        else:
            messages.warning(request, "Veuillez finaliser le paiement pour accéder au cours.")
            return redirect('formations:detail_session', session_id=session.id)

    lecons = list(formation.lecons.all())
    if not lecons:
        messages.info(request, "Ce cours n'a pas encore de contenu disponible.")
        return redirect('formations:detail_session', session_id=session.id)

    current_lecon = None
    if lecon_id:
        current_lecon = get_object_or_404(Lecon, id=lecon_id)
    else:
        current_lecon = lecons[0]

    # Navigation prev/next
    prev_lecon = None
    next_lecon = None
    for i, lec in enumerate(lecons):
        if lec.id == current_lecon.id:
            if i > 0:
                prev_lecon = lecons[i - 1]
            if i < len(lecons) - 1:
                next_lecon = lecons[i + 1]
            break

    # Marquer comme complétée et recalculer la progression
    if inscription and not inscription.completed_lessons.filter(id=current_lecon.id).exists():
        inscription.completed_lessons.add(current_lecon)
        inscription.recalculate_progression()

    return render(request, 'formations/course_player.html', {
        'session': session,
        'formation': formation,
        'lecons': lecons,
        'current_lecon': current_lecon,
        'prev_lecon': prev_lecon,
        'next_lecon': next_lecon,
        'inscription': inscription,
    })