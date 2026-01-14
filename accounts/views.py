from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm
from formations.models import Inscription
from blog.models import Ressource
from library.models import AchatLivre

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ResourcesView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/resources.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resources'] = Ressource.objects.all()
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inscriptions'] = Inscription.objects.filter(user=self.request.user)
        context['mes_livres'] = AchatLivre.objects.filter(user=self.request.user).select_related('livre').order_by('-date_achat')
        return context

from django.core.mail import send_mail

def simuler_paiement(request, inscription_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    inscription = get_object_or_404(Inscription, id=inscription_id, user=request.user)
    
    if inscription.statut_paiement != 'paid':
        inscription.statut_paiement = 'paid'
        inscription.save()
        
        # Email Notification Logic
        subject = f"Confirmation de paiement - {inscription.session.programme.titre}"
        message = f"Bonjour {request.user.username},\n\nVotre paiement pour la session de {inscription.session.programme.titre} a été validé avec succès.\n\nL'équipe ATJ."
        try:
            send_mail(subject, message, 'no-reply@atj.com', [request.user.email])
            messages.success(request, f"Paiement validé ! Un email de confirmation a été envoyé à {request.user.email}")
        except Exception as e:
            messages.warning(request, f"Paiement validé, mais échec de l'envoi d'email: {e}")
            
    return redirect('accounts:dashboard')
