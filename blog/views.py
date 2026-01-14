from django.shortcuts import render, get_object_or_404
from .models import Article, Ressource

def blog_index(request):
    articles = Article.objects.order_by('-date_publication')
    return render(request, 'blog/index.html', {'articles': articles})

def resource_detail(request, resource_id):
    resource = get_object_or_404(Ressource, id=resource_id)
    return render(request, 'blog/resource_detail.html', {'resource': resource})
