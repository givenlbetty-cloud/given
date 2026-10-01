from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from blog.models import Article, Event
from .forms import ContactForm
from .models import SiteSettings, TeamMember
from .brochure import MISSION, VISION, PILIERS

class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mission_depliant'] = MISSION
        context['vision_depliant'] = VISION
        context['piliers'] = PILIERS
        return context

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
        
        context['piliers'] = PILIERS
        return context

class ContactView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form_available'] = self.email_recipient is not None
        return context

    @property
    def email_recipient(self):
        site = SiteSettings.objects.first()
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            return None
        return site.contact_email if site and site.contact_email else None

    def form_valid(self, form):
        recipient = self.email_recipient
        if not recipient:
            messages.warning(self.request, "Le formulaire n'est pas disponible. Veuillez nous appeler au numéro indiqué.")
            return redirect('contact')

        nom = form.cleaned_data['nom']
        email = form.cleaned_data['email']
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']

        full_message = f"Message de {nom} ({email}):\n\n{message}"
        
        try:
            send_mail(
                subject=f"[Contact ATJ] {sujet}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception:
            messages.error(self.request, "Le message n'a pas pu être envoyé. Veuillez nous contacter par téléphone.")
            return redirect('contact')

        messages.success(self.request, "Votre message a bien été envoyé !")
        return super().form_valid(form)
