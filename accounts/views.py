from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .forms import CustomUserCreationForm
from .models import CustomUser
from formations.models import Inscription, Paiement
from blog.models import Ressource
from library.models import AchatLivre

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Vous êtes déjà membre de l'académie !")
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        # Backend explicite requis car AUTHENTICATION_BACKENDS multiples (allauth)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return redirect(self.success_url)

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Inscriptions stats
        context['total_inscriptions'] = user.inscriptions.count()
        context['active_inscriptions'] = user.inscriptions.filter(statut_validation=True).count()
        
        # Library stats
        books = user.achatlivre_set.all()
        context['total_books'] = books.count()
        context['completed_books'] = books.filter(est_termine=True).count()
        
        if context['total_books'] > 0:
            context['book_progress'] = int((context['completed_books'] / context['total_books']) * 100)
        else:
            context['book_progress'] = 0
            
        return context


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

def simuler_paiement(request, inscription_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    inscription = get_object_or_404(Inscription, id=inscription_id, user=request.user)
    
    if request.method == 'POST':
        if inscription.statut_paiement != 'paid':
            Paiement.objects.create(
                user=request.user,
                inscription=inscription,
                montant=0.00,
                valide=True,
                transaction_id=f"SIM-{inscription.id}-{request.user.id}"
            )
            
            inscription.statut_paiement = 'paid'
            inscription.save()
            
            subject = f"Confirmation de paiement - {inscription.session.programme.titre}"
            message = f"Bonjour {request.user.username},\n\nVotre paiement pour la session de {inscription.session.programme.titre} a été validé avec succès.\n\nL'équipe ATJ."
            try:
                send_mail(subject, message, 'no-reply@atj.com', [request.user.email])
                messages.success(request, f"Paiement validé ! Un email de confirmation a été envoyé à {request.user.email}")
            except Exception as e:
                messages.warning(request, f"Paiement validé, mais échec de l'envoi d'email: {e}")
                
        return redirect('accounts:dashboard')

    return render(request, 'accounts/paiement_simulation.html', {'inscription': inscription})