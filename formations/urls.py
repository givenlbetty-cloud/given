from django.urls import path
from . import views

app_name = 'formations'

urlpatterns = [
    path('', views.liste_programmes, name='liste'),
    path('inscrire/<int:session_id>/', views.inscrire_session, name='inscrire_session'),
    path('paiement/<int:session_id>/', views.paiement_session, name='paiement_session'),
    path('process-payment/<int:session_id>/', views.process_payment, name='process_payment'),
    path('session/<int:session_id>/', views.detail_session, name='detail_session'),
    path('cours/<int:session_id>/', views.course_content, name='course_content_default'),
    path('cours/<int:session_id>/lecon/<int:lecon_id>/', views.course_content, name='course_content'),
]
