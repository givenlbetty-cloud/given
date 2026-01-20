from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Article, Ressource, Event
from itertools import chain
from operator import attrgetter

def blog_index(request):
    articles = Article.objects.all()
    events = Event.objects.all()
    
    # Annotate types to distinguish in template
    for a in articles:
        a.type_content = 'article'
        a.date_display = a.date_publication
        
    for e in events:
        e.type_content = 'event'
        e.date_display = e.date
        
    # Combine and sort by newest first
    feed_items = sorted(
        chain(articles, events),
        key=attrgetter('date_display'),
        reverse=True
    )
    
    return render(request, 'blog/index.html', {'feed_items': feed_items})

def resource_detail(request, resource_id):
    resource = get_object_or_404(Ressource, id=resource_id)
    return render(request, 'blog/resource_detail.html', {'resource': resource})

class MentorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'mentor' or self.request.user.is_superuser

class ArticleCreateView(LoginRequiredMixin, MentorRequiredMixin, CreateView):
    model = Article
    fields = ['titre', 'image', 'contenu']
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('mentoring:dashboard')

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        messages.success(self.request, "Article publié avec succès !")
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['titre', 'image', 'contenu']
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('mentoring:dashboard')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.auteur or self.request.user.is_superuser

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'blog/article_confirm_delete.html'
    success_url = reverse_lazy('mentoring:dashboard')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.auteur or self.request.user.is_superuser
