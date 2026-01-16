from django.urls import path
from . import views

app_name = 'formations'

urlpatterns = [
    path('', views.liste_programmes, name='liste'),
    path('inscrire/<int:session_id>/', views.inscrire_session, name='inscrire_session'),
    path('session/<int:session_id>/', views.detail_session, name='detail_session'),
]
