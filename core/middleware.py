"""
🔐 Middleware Basic Authentication pour environnement BETA
Protège l'accès au site par mot de passe
"""

import base64
import os
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class BasicAuthMiddleware(MiddlewareMixin):
    """
    Middleware pour protéger l'accès en Basic Auth.
    
    À utiliser UNIQUEMENT en environnement beta/test.
    Activer via ENABLE_BASIC_AUTH=True dans .env.beta
    """

    def __init__(self, get_response):
        super().__init__(get_response)
        self.enable_basic_auth = os.getenv('ENABLE_BASIC_AUTH', 'False') == 'True'
        self.username = os.getenv('BASIC_AUTH_USERNAME', 'beta_user')
        self.password = os.getenv('BASIC_AUTH_PASSWORD', 'change_me')
        
        # Chemins exempt de Basic Auth (admin, API public, etc.)
        self.exempt_paths = [
            '/health/',
            '/api/public/',
            '/.well-known/',
            '/static/',
            '/media/',
        ]

    def process_request(self, request):
        """Vérifier les credentials Basic Auth"""
        
        # Ignorer si Basic Auth désactivé
        if not self.enable_basic_auth:
            return None

        # Ignorer les chemins exempt
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return None

        # Vérifier l'en-tête Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header.startswith('Basic '):
            return self._prompt_credentials()

        try:
            # Décoder les credentials
            auth_encoded = auth_header.split(' ')[1]
            auth_decoded = base64.b64decode(auth_encoded).decode('utf-8')
            username, password = auth_decoded.split(':', 1)

            # Vérifier les credentials
            if username == self.username and password == self.password:
                # ✅ Authentification réussie
                return None
            else:
                # ❌ Credentials invalides
                return self._prompt_credentials()

        except (IndexError, ValueError):
            return self._prompt_credentials()

    def _prompt_credentials(self):
        """Retourner une réponse 401 avec demande d'authentification"""
        response = HttpResponse(
            '<html><body><h1>⚠️ ACCÈS PROTÉGÉ</h1>'
            '<p>Cette version de test est protégée par mot de passe.</p>'
            '<p>Veuillez entrer vos identifiants Basic Auth.</p>'
            '</body></html>',
            status=401,
            content_type='text/html'
        )
        response['WWW-Authenticate'] = 'Basic realm="ATJ Beta Testing"'
        return response


class BetaEnvironmentHeaderMiddleware(MiddlewareMixin):
    """
    Ajoute des headers indiquant qu'on est en environnement BETA.
    Utile pour le debugging et les tests.
    """

    def process_response(self, request, response):
        """Ajouter headers BETA"""
        response['X-Environment'] = 'BETA'
        response['X-Database'] = 'Separate Beta Database'
        response['X-Version'] = 'Beta v1.0'
        return response
