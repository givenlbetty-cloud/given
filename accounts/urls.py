from django.urls import path
from .views import SignUpView, DashboardView, ResourcesView, simuler_paiement

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('resources/', ResourcesView.as_view(), name='resources'),
    path('pay/<int:inscription_id>/', simuler_paiement, name='simuler_paiement'),
]
