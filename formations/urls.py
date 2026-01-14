from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_programmes, name='programmes'),
    path('inscrire/<int:session_id>/', views.inscrire_session, name='inscrire_session'),
]
