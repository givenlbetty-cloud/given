from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.http import FileResponse, Http404, JsonResponse
from .models import Livre, AchatLivre, Note, Avis, Favori
import mimetypes
import os

def liste_livres(request):
    categorie = request.GET.get('categorie')
    query = request.GET.get('q')
    
    livres_qs = Livre.objects.annotate(note_moyenne=Avg('avis__note')).order_by('-date_creation')

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

def detail_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    
    achat = None
    is_favori = False
    
    if request.user.is_authenticated:
        try:
            achat = AchatLivre.objects.get(user=request.user, livre=livre)
        except AchatLivre.DoesNotExist:
            achat = None
        is_favori = Favori.objects.filter(user=request.user, livre=livre).exists()
        
    avis_list = livre.avis.all().order_by('-date_creation')
    note_moyenne = avis_list.aggregate(moyenne=Avg('note'))['moyenne']
    
    if request.method == 'POST' and 'submit_avis' in request.POST:
        if not request.user.is_authenticated:
             return redirect('login')
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
        'note_moyenne': note_moyenne,
        'is_favori': is_favori
    })

@login_required
def lire_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    
    # MODIFICATION : Tous les livres sont gratuits et accessibles
    # On crée ou récupère l'objet achat pour le suivi de lecture uniquement
    achat, created = AchatLivre.objects.get_or_create(user=request.user, livre=livre)

    # Gestion des notes
    if request.method == 'POST':
        if 'update_progress' in request.POST:
            page = request.POST.get('page')
            total_pages = request.POST.get('total_pages')
            
            if achat and page:
                try:
                    current_page = int(page)
                    if current_page < 1:
                        raise ValueError
                    if total_pages:
                        total = int(total_pages)
                        if total < 1:
                            raise ValueError
                        current_page = min(current_page, total)
                        achat.derniere_page_lue = current_page
                        achat.est_termine = current_page >= total
                    else:
                        achat.derniere_page_lue = current_page

                    achat.save()
                    return JsonResponse({
                        'status': 'ok', 
                        'page': current_page,
                        'completed': achat.est_termine
                    })
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid page number'}, status=400)
                
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
    
    content = None
    is_pdf = False
    is_text = False
    if livre.fichier:
        extension = os.path.splitext(livre.fichier.name)[1].lower()
        is_pdf = extension == '.pdf'
        is_text = extension == '.txt'
        if is_text:
            try:
                livre.fichier.open('rb')
                try:
                    content = livre.fichier.read().decode('utf-8')
                finally:
                    livre.fichier.close()
            except Exception:
                content = "Impossible de lire le contenu du fichier."

    return render(request, 'library/lecture.html', {
        'livre': livre,
        'notes': notes,
        'last_page': last_page,
        'content': content,
        'is_pdf': is_pdf,
        'is_text': is_text,
    })


def _book_file_response(livre, *, as_attachment):
    filename = os.path.basename(livre.fichier.name)
    extension = os.path.splitext(filename)[1].lower()
    content_type = (
        'application/pdf'
        if extension == '.pdf'
        else mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    )
    file_object = livre.fichier.open('rb')
    return FileResponse(
        file_object,
        as_attachment=as_attachment,
        filename=filename,
        content_type=content_type,
    )


@login_required
def lire_fichier_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    if not livre.fichier:
        raise Http404("No file is associated with this book.")
    return _book_file_response(livre, as_attachment=False)


@login_required
def acheter_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    
    # MODIFICATION : Tous les livres sont considérés comme gratuits
    # Ajout direct à la bibliothèque
    obj, created = AchatLivre.objects.get_or_create(user=request.user, livre=livre)
    if created:
        messages.success(request, f"'{livre.titre}' a été ajouté à votre bibliothèque gratuitement.")
    else:
        messages.info(request, "Ce livre est déjà dans votre bibliothèque.")
    return redirect('library:detail', livre_id=livre.id)
    
    # Le code ci-dessous est désactivé car tout devint gratuit
    """
    if livre.is_free():
         messages.info(request, "Vous avez déjà acheté ce livre.")
         return redirect('library:detail', livre_id=livre.id)
    
    if request.method == 'POST':
        # Simuler le paiement
        AchatLivre.objects.create(user=request.user, livre=livre)
        messages.success(request, f"Votre achat de '{livre.titre}' a été confirmé !")
        return redirect('library:detail', livre_id=livre.id)
        
    return render(request, 'library/paiement.html', {'livre': livre})
    """


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
    
    # Auto-add to library on download if not present
    AchatLivre.objects.get_or_create(user=request.user, livre=livre)
    
    if livre.fichier:
        try:
            return _book_file_response(livre, as_attachment=True)
        except Exception:
            messages.error(request, "Le fichier de ce livre est temporairement indisponible.")
            return redirect('library:detail', livre_id=livre.id)
    else:
        messages.error(request, "Aucun fichier associé à ce livre.")
        return redirect('library:detail', livre_id=livre.id)
