from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Mentor
from blog.models import Article
from chat.models import Thread
from django.db.models import Q

def mentor_list(request):
    query = request.GET.get('q')
    if query:
        mentors = Mentor.objects.filter(
            Q(user__username__icontains=query) | 
            Q(expertise__icontains=query)
        )
    else:
        mentors = Mentor.objects.all()
    return render(request, 'mentoring/list.html', {'mentors': mentors, 'query': query})

def mentor_detail(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)
    # Increment views
    mentor.views_count += 1
    mentor.save()
    return render(request, 'mentoring/detail.html', {'mentor': mentor})

@login_required
def mentor_dashboard(request):
    if request.user.role != 'mentor' and not request.user.is_superuser:
        return redirect('home')
    
    # Récupérer les articles du mentor
    articles = Article.objects.filter(auteur=request.user).order_by('-date_publication')
    
    # Récupérer les conversations récentes
    threads = request.user.threads.all().order_by('-updated_at')[:5]
    
    # Récupérer le profil mentor
    try:
        mentor_profile = request.user.mentor_profile
    except Mentor.DoesNotExist:
        # Créer un profil par défaut si inexistant
        mentor_profile = Mentor.objects.create(user=request.user, bio="Bio à compléter", expertise="Non spécifié")

    return render(request, 'mentoring/dashboard.html', {
        'articles': articles,
        'threads': threads,
        'mentor_profile': mentor_profile
    })
