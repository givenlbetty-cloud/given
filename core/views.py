from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from blog.models import Article, Event
from .forms import ContactForm
from .models import TeamMember

class AboutView(TemplateView):
    template_name = 'core/about.html'

class TeamView(TemplateView):
    template_name = 'core/team.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        return context

class HomeView(TemplateView):
    template_name = 'core/home_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Données statiques pour les 5 piliers (pour le prototype UI)
        # On pourrait aussi les récupérer dynamiquement si Programme a un champ catégorie
        context['piliers'] = [
            ('art_oratoire', 'Art Oratoire', 'bi-mic-fill', '#800020', 'offline', 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
            ('leadership', 'Leadership', 'bi-lightning-charge-fill', '#2c3e50', 'offline', 'https://images.unsplash.com/photo-1552664730-d307ca884978?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
            ('informatique', 'Informatique', 'bi-laptop', '#2980b9', 'online', 'https://images.unsplash.com/photo-1587620962725-abab7fe55159?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
            ('langues', 'Langues', 'bi-translate', '#e67e22', 'online', 'https://images.unsplash.com/photo-1546410531-bb4caa6b424d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
            ('affaires', 'Affaires', 'bi-briefcase-fill', '#27ae60', 'hybrid', 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ]
        return context

class ContactView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Send email
        nom = form.cleaned_data['nom']
        email = form.cleaned_data['email']
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']

        full_message = f"Message de {nom} ({email}):\n\n{message}"
        
        try:
            send_mail(
                subject=f"[Contact ATJ] {sujet}",
                message=full_message,
                from_email='contact-form@atj.com',
                recipient_list=['admin@atj.com'],
                fail_silently=False,
            )
            messages.success(self.request, "Votre message a bien été envoyé !")
        except Exception as e:
            messages.error(self.request, f"Erreur lors de l'envoi : {e}")
            
        return super().form_valid(form)
