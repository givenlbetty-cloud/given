from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Programme, Session, Inscription, Lecon, Chapitre
from django.contrib import messages
from .decorators import payment_required

def liste_programmes(request):
    query = request.GET.get('q')
    categorie = request.GET.get('categorie')
    # Filter only published programs for the public list
    programmes = Programme.objects.filter(est_publie=True)
    
    if query:
        programmes = programmes.filter(titre__icontains=query)
    
    if categorie:
        programmes = programmes.filter(categorie=categorie)
        
    return render(request, 'formations/liste.html', {
        'programmes': programmes,
        'query': query,
        'categorie': categorie
    })

@login_required
def inscrire_session(request, session_id):
    if request.method == 'POST':
        session = get_object_or_404(Session, id=session_id)
        # Check if already enrolled
        inscription, created = Inscription.objects.get_or_create(user=request.user, session=session)
        
        if created:
             # Check if free
             if session.programme.prix <= 0:
                 inscription.statut_paiement = 'paid'
                 inscription.statut_validation = True
                 inscription.save()
                 messages.success(request, f"Inscription confirmée pour {session.programme.titre}.")
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

    return redirect('programmes')

@login_required
def paiement_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    inscription = get_object_or_404(Inscription, user=request.user, session=session)
    
    if inscription.statut_paiement == 'paid':
        return redirect('formations:detail_session', session_id=session.id)
        
    return render(request, 'formations/paiement.html', {
        'session': session,
        'formation': session.programme,
        'inscription': inscription
    })

@login_required
def process_payment(request, session_id):
    if request.method == 'POST':
        session = get_object_or_404(Session, id=session_id)
        inscription = get_object_or_404(Inscription, user=request.user, session=session)
        
        # Simulation de paiement réussi
        import uuid
        from .models import Paiement
        
        # Update Inscription
        inscription.statut_paiement = 'paid'
        inscription.statut_validation = True
        inscription.save()
        
        # Create Paiement Record
        Paiement.objects.create(
            user=request.user,
            inscription=inscription,
            montant=session.programme.prix,
            valide=True,
            transaction_id=str(uuid.uuid4())
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

    chapitres = session.programme.chapitres.prefetch_related('lecons').all()

    return render(request, 'formations/detail_session.html', {
        'session': session,
        'inscription': inscription,
        'chapitres': chapitres
    })

@login_required
def course_content(request, session_id, lecon_id=None):
    session = get_object_or_404(Session, id=session_id)
    program = session.programme
    
    # Check inscription
    inscription = Inscription.objects.filter(user=request.user, session=session).first()
    if not inscription:
        messages.warning(request, "Veuillez vous inscrire pour accéder au cours.")
        return redirect('formations:detail_session', session_id=session.id)
    
    # Vérification de paiement pour les formations payantes
    if program.prix > 0 and inscription.statut_paiement != 'paid':
        # Vérifier si la leçon demandée est gratuite (teaser)
        if lecon_id:
            lecon = get_object_or_404(Lecon, id=lecon_id)
            if not lecon.est_gratuit:
                messages.warning(request, "Veuillez finaliser le paiement pour accéder à ce cours.")
                return redirect('formations:detail_session', session_id=session.id)
        else:
            messages.warning(request, "Veuillez finaliser le paiement pour accéder au cours.")
            return redirect('formations:detail_session', session_id=session.id)

    # Récupérer la structure du cours
    chapitres = program.chapitres.prefetch_related('lecons').all()
    
    current_lecon = None
    if lecon_id:
        current_lecon = get_object_or_404(Lecon, id=lecon_id)
    else:
        first_chap = chapitres.first()
        if first_chap:
            current_lecon = first_chap.lecons.first()
            
    if not current_lecon:
        messages.info(request, "Ce cours n'a pas encore de contenu disponible.")
        return redirect('formations:detail_session', session_id=session.id)
        
    # Navigation logic (Prev/Next)
    all_lecons = []
    for chap in chapitres:
        for lecon in chap.lecons.all():
            all_lecons.append(lecon)
            
    prev_lecon = None
    next_lecon = None
    
    for i, lec in enumerate(all_lecons):
        if lec.id == current_lecon.id:
            if i > 0:
                prev_lecon = all_lecons[i-1]
            if i < len(all_lecons) - 1:
                next_lecon = all_lecons[i+1]
            break
    
    # Mettre à jour la progression (estimation basée sur la position)
    if all_lecons and inscription:
        total = len(all_lecons)
        current_idx = next((i for i, lec in enumerate(all_lecons) if lec.id == current_lecon.id), 0)
        progression = int((current_idx + 1) / total * 100) if total > 0 else 0
        if progression > inscription.progression:
            inscription.progression = progression
            inscription.save(update_fields=['progression'])
            
    return render(request, 'formations/course_player.html', {
        'session': session,
        'program': program,
        'chapitres': chapitres,
        'current_lecon': current_lecon,
        'prev_lecon': prev_lecon,
        'next_lecon': next_lecon,
        'inscription': inscription
    })