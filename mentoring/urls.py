from django.urls import path
from . import views

urlpatterns = [
    path('', views.mentor_list, name='mentors'),
    path('<int:mentor_id>/', views.mentor_detail, name='mentor_detail'),
]
