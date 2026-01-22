from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import HomeView, ContactView, TeamView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('equipe/', TeamView.as_view(), name='team'),
    path('contact/', ContactView.as_view(), name='contact'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('formations/', include('formations.urls')),
    path('mentoring/', include('mentoring.urls')),
    path('chat/', include('chat.urls')),
    path('blog/', include('blog.urls')),
    path('library/', include('library.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
