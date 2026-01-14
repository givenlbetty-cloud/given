from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.liste_livres, name='liste'),
    path('<int:livre_id>/', views.detail_livre, name='detail'),
    path('<int:livre_id>/lire/', views.lire_livre, name='lecture'),
    path('<int:livre_id>/acheter/', views.acheter_livre, name='acheter'),
    path('<int:livre_id>/download/', views.telecharger_livre, name='download'),
    path('<int:livre_id>/favori/', views.toggle_favori, name='toggle_favori'),
]