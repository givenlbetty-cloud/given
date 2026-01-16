from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_index, name='index'),
    path('creer/', views.ArticleCreateView.as_view(), name='creer_article'),
    path('modifier/<int:pk>/', views.ArticleUpdateView.as_view(), name='modifier_article'),
    path('supprimer/<int:pk>/', views.ArticleDeleteView.as_view(), name='supprimer_article'),
    path('resource/<int:resource_id>/', views.resource_detail, name='detail'),
]
