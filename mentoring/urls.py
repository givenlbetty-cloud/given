from django.urls import path
from . import views

app_name = 'mentoring'

urlpatterns = [
    path('', views.mentor_list, name='liste'),
    path('dashboard/', views.mentor_dashboard, name='dashboard'),
    path('<int:mentor_id>/', views.mentor_detail, name='detail'),
]
