from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('resource/<int:resource_id>/', views.resource_detail, name='resource_detail'),
]
