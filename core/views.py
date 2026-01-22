from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from blog.models import Article, Event
from .forms import ContactForm
from .models import TeamMember

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
            ('art_oratoire', 'Art Oratoire', 'bi-mic-fill', '#800020', 'offline'),
            ('leadership', 'Leadership', 'bi-lightning-charge-fill', '#2c3e50', 'offline'),
            ('informatique', 'Informatique', 'bi-laptop', '#2980b9', 'online'),
            ('langues', 'Langues', 'bi-translate', '#e67e22', 'online'),
            ('affaires', 'Affaires', 'bi-briefcase-fill', '#27ae60', 'hybrid'),
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
