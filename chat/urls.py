from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('t/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
]
