from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, Http404, JsonResponse
from .models import Livre, AchatLivre, Note, Avis, Favori

def liste_livres(request):
    categorie = request.GET.get('categorie')
    query = request.GET.get('q')
    
    livres_qs = Livre.objects.all().order_by('-date_creation')

    if categorie:
        livres_qs = livres_qs.filter(categorie=categorie)
    
    if query:
        livres_qs = livres_qs.filter(
            Q(titre__icontains=query) | 
            Q(auteur__icontains=query)
        )
    
    paginator = Paginator(livres_qs, 9)  # 9 livres par page
    page_number = request.GET.get('page')
    livres = paginator.get_page(page_number)
    
    owned_books = set()
    if request.user.is_authenticated:
        owned_books = set(AchatLivre.objects.filter(user=request.user).values_list('livre_id', flat=True))
    
    categories = Livre.CATEGORIES
    return render(request, 'library/liste.html', {
        'livres': livres, 
        'categories': categories, 
        'current_category': categorie,
        'query': query,
        'owned_books': owned_books
    })

@login_required
def detail_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    try:
        achat = AchatLivre.objects.get(user=request.user, livre=livre)
    except AchatLivre.DoesNotExist:
        achat = None
        
    is_favori = Favori.objects.filter(user=request.user, livre=livre).exists()
        
    avis_list = livre.avis.all().order_by('-date_creation')
    
    if request.method == 'POST' and 'submit_avis' in request.POST:
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        if note and commentaire:
            Avis.objects.create(user=request.user, livre=livre, note=note, commentaire=commentaire)
            messages.success(request, "Merci pour votre avis !")
            return redirect('library:detail', livre_id=livre.id)

    return render(request, 'library/detail.html', {
        'livre': livre, 
        'achat': achat, 
        'avis_list': avis_list,
        'is_favori': is_favori
    })

@login_required
def lire_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    
    # Vérification des droits d'accès
    achat = None
    if not livre.is_free():
        try:
            achat = AchatLivre.objects.get(user=request.user, livre=livre)
        except AchatLivre.DoesNotExist:
             messages.error(request, "Vous devez acheter ce livre pour le lire.")
             return redirect('library:detail', livre_id=livre.id)
    else:
        # Si le livre est gratuit, on crée ou récupère l'objet achat pour le suivi
        achat, created = AchatLivre.objects.get_or_create(user=request.user, livre=livre)

    # Gestion des notes
    if request.method == 'POST':
        if 'update_progress' in request.POST:
            page = request.POST.get('page')
            if achat and page:
                achat.derniere_page_lue = int(page)
                achat.save()
                return JsonResponse({'status': 'ok'})
                
        contenu = request.POST.get('contenu')
        page = request.POST.get('page')
        if contenu:
            Note.objects.create(
                user=request.user, 
                livre=livre, 
                contenu=contenu,
                page_reference=page if page else None
            )
            messages.success(request, "Note ajoutée !")
            return redirect('library:lecture', livre_id=livre.id)

    notes = Note.objects.filter(user=request.user, livre=livre).order_by('-date_creation')
    last_page = achat.derniere_page_lue if achat else 1
    
    # Check for text file content
    content = None
    is_pdf = True
    if livre.fichier:
        if livre.fichier.name.lower().endswith('.txt'):
            is_pdf = False
            try:
                with open(livre.fichier.path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                content = "Impossible de lire le contenu du fichier."
        elif not livre.fichier.name.lower().endswith('.pdf'):
            # Fallback for other types if any, or assume PDF for now if not txt
            # But the template uses PDF.js, so non-PDFs won't work there either.
            pass

    return render(request, 'library/lecture.html', {
        'livre': livre, 
        'notes': notes, 
        'last_page': last_page,
        'content': content,
        'is_pdf': is_pdf
    })

@login_required
def acheter_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    
    if livre.is_free():
        # Pour les livres gratuits, on les ajoute directement
        obj, created = AchatLivre.objects.get_or_create(user=request.user, livre=livre)
        if created:
            messages.success(request, f"'{livre.titre}' a été ajouté à votre bibliothèque.")
        else:
            messages.info(request, "Ce livre est déjà dans votre bibliothèque.")
        return redirect('library:detail', livre_id=livre.id)
    
    if AchatLivre.objects.filter(user=request.user, livre=livre).exists():
         messages.info(request, "Vous avez déjà acheté ce livre.")
         return redirect('library:detail', livre_id=livre.id)
    
    if request.method == 'POST':
        # Simuler le paiement
        AchatLivre.objects.create(user=request.user, livre=livre)
        messages.success(request, f"Votre achat de '{livre.titre}' a été confirmé !")
        return redirect('library:detail', livre_id=livre.id)
        
    return render(request, 'library/paiement.html', {'livre': livre})


@login_required
def toggle_favori(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    favori, created = Favori.objects.get_or_create(user=request.user, livre=livre)
    if not created:
        favori.delete()
        messages.info(request, "Retiré des favoris.")
    else:
        messages.success(request, "Ajouté aux favoris !")
    
    return redirect('library:detail', livre_id=livre.id)

@login_required
def telecharger_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    
    # Check permissions
    if not livre.is_free() and not AchatLivre.objects.filter(user=request.user, livre=livre).exists():
        messages.error(request, "Vous devez acheter ce livre pour le télécharger.")
        return redirect('library:detail', livre_id=livre.id)
    
    if livre.fichier:
        response = FileResponse(livre.fichier.open(), as_attachment=True)
        return response
    else:
        raise Http404("Fichier introuvable")
