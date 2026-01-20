from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Programme, Session, Inscription, Lecon, Chapitre
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
    # L'objet inscription est déjà récupéré et vérifié par le décorateur @payment_required
    # Il est disponible via request.inscription
    inscription = getattr(request, 'inscription', None)
    
    if not inscription:
        # Fallback de sécurité au cas où le décorateur serait mal utilisé
        inscription = get_object_or_404(Inscription, user=request.user, session=session)

    # Fetch Syllabus for display
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
    
    # Ici on pourrait ajouter une vérification de paiement stricte
    # if inscription.statut_paiement != 'paid' and not current_lecon.est_gratuit: ...

    # Récupérer la structure du cours optimisée
    chapitres = program.chapitres.prefetch_related('lecons').all()
    
    current_lecon = None
    if lecon_id:
        current_lecon = get_object_or_404(Lecon, id=lecon_id)
    else:
        # Get first available lesson
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
            
    return render(request, 'formations/course_player.html', {
        'session': session,
        'program': program,
        'chapitres': chapitres,
        'current_lecon': current_lecon,
        'prev_lecon': prev_lecon,
        'next_lecon': next_lecon,
        'inscription': inscription
    }) 
    # But adhering to specs: "S'inscrire et Payer".
    inscription = get_object_or_404(Inscription, user=request.user, session=session)
    
    if inscription.statut_paiement != 'paid':
         messages.warning(request, "Veuillez finaliser le paiement pour accéder au cours.")
         return redirect('accounts:dashboard')

    programme = session.programme
    chapitres = programme.chapitres.prefetch_related('lecons').all()
    
    # Determine current lesson
    if lecon_id:
        current_lecon = get_object_or_404(Lecon, id=lecon_id)
    else:
        # Default to first lesson of first chapter
        first_chap = chapitres.first()
        current_lecon = first_chap.lecons.first() if first_chap else None

    # Navigation Logic
    all_lessons = []
    for chap in chapitres:
        all_lessons.extend(chap.lecons.all())
    
    prev_lecon = None
    next_lecon = None
    
    if current_lecon and current_lecon in all_lessons:
        idx = all_lessons.index(current_lecon)
        if idx > 0:
            prev_lecon = all_lessons[idx-1]
        if idx < len(all_lessons) - 1:
            next_lecon = all_lessons[idx+1]

    context = {
        'session': session,
        'programme': programme,
        'chapitres': chapitres,
        'current_lecon': current_lecon,
        'prev_lecon': prev_lecon,
        'next_lecon': next_lecon,
    }
    return render(request, 'formations/course_player.html', context)
