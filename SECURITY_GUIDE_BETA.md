# 🔐 GUIDE DE SÉCURITÉ - ENVIRONNEMENT BETA

**Objectif:** Assurer une isolation totale entre l'environnement de test (beta) et la production.

---

## 📋 PRINCIPES FONDAMENTAUX

### 1. Séparation Complète

| Élément | Production | Beta | Isolation |
|---------|-----------|------|-----------|
| **Base de Données** | `db.sqlite3` | `db_beta.sqlite3` | ✅ Complète |
| **Médias Uploads** | `media/` | `media_beta/` | ✅ Complète |
| **Configuration** | `settings.py` | `settings_beta.py` | ✅ Complète |
| **Variables ENV** | `.env` | `.env.beta` | ✅ Complète |
| **Git Branch** | `main` | `beta-test` | ✅ Complète |
| **Static Files** | `staticfiles/` | `staticfiles_beta/` | ✅ Complète |

### 2. Aucune Donnée Partagée

- ❌ Jamais utiliser la BD production en beta
- ❌ Jamais stocker les uploads beta dans `media/`
- ❌ Jamais commiter `.env.beta` sur git
- ❌ Jamais utiliser des clés API LIVE en beta
- ❌ Jamais envoyer de vrais emails depuis beta

### 3. Protections Multi-Niveaux

```
┌─────────────────────────────────┐
│  1. Basic Auth Middleware       │  ← Demande mot de passe
├─────────────────────────────────┤
│  2. Isolation Application       │  ← settings_beta.py séparé
├─────────────────────────────────┤
│  3. Isolation Données           │  ← BD séparée + médias séparés
├─────────────────────────────────┤
│  4. Isolation Infrastructure    │  ← Services tiers en TEST mode
├─────────────────────────────────┤
│  5. Isolation Déploiement       │  ← Domaine distinct + certificat
└─────────────────────────────────┘
```

---

## 🔐 PROTECTION 1: BASIC AUTH (Accès)

### Configuration

```python
# .env.beta
ENABLE_BASIC_AUTH=True
BASIC_AUTH_USERNAME=beta_user
BASIC_AUTH_PASSWORD=very_secure_password_min_8_chars
```

### Implémentation (Middleware)

```python
# core/middleware.py
class BasicAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Vérifier les credentials avant d'accéder au site
        # Envoyer 401 + demande d'authentification si incorrects
```

### Utilisation

```bash
# Curl avec Basic Auth
curl -u beta_user:password http://localhost:8000/

# Browser: Demande d'identifiants au premier accès
# Entrez: beta_user / password
```

---

## 📊 PROTECTION 2: ISOLATION APPLICATION

### settings_beta.py

```python
# Configuration dédiée (ne pas partager avec main)
from dotenv import load_dotenv

load_dotenv('.env.beta')  # Charger .env.beta, pas .env

# Chaque paramètre est séparé:
DEBUG = os.getenv('DEBUG', 'True') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')  # Clé différente
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
DATABASES['default']['NAME'] = 'db_beta.sqlite3'
MEDIA_ROOT = 'media_beta'
```

### Lancement

```bash
# Utiliser settings_beta.py
python3 manage.py runserver --settings=atj_site.settings_beta

# OU
DJANGO_SETTINGS_MODULE=atj_site.settings_beta python3 manage.py runserver
```

---

## 🗂️ PROTECTION 3: ISOLATION DONNÉES

### Base de Données

```bash
# Production (JAMAIS modifier!)
db.sqlite3

# Beta (données de test uniquement)
db_beta.sqlite3

# Elles sont TOTALEMENT séparées
# Pas de relation, pas de synchronisation
```

**Vérification:**

```bash
# Confirmer qu'elles sont différentes
ls -la db.sqlite3 db_beta.sqlite3
# Doivent avoir des inodes différents (inode column)
```

### Médias

```bash
# Production
media/
├── articles/
├── livres_fichiers/
└── programmes/

# Beta (SÉPARÉ)
media_beta/
├── articles/  (uploads de test seulement)
├── livres_fichiers/
└── programmes/
```

**Configuration:**

```python
# .env.beta
MEDIA_ROOT=media_beta
MEDIA_URL=/media_beta/

# Tous les uploads vont dans media_beta/, pas media/
```

---

## 💳 PROTECTION 4: SERVICES TIERS (Sandbox)

### Stripe

```python
# .env.beta - UNIQUEMENT clés TEST

✅ CORRECT:
STRIPE_PUBLIC_KEY=pk_test_51234567890abcdef
STRIPE_SECRET_KEY=sk_test_51234567890abcdef

❌ DANGEREUX:
STRIPE_PUBLIC_KEY=pk_live_51234567890abcdef
STRIPE_SECRET_KEY=sk_live_51234567890abcdef
```

**Validation:**

```python
# settings_beta.py vérifie automatiquement:
if STRIPE_SECRET_KEY.startswith('sk_live_'):
    raise ValueError(
        "⚠️  ERREUR CRITIQUE: Clé PRODUCTION Stripe détectée!"
    )
```

### Email

```python
# Ne JAMAIS envoyer de vrais emails en beta!

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Les emails s'affichent en console:
# ─────────────────────────────────
# Content-Type: text/plain; charset="utf-8"
# MIME-Version: 1.0
# Content-Transfer-Encoding: 7bit
# Subject: Bienvenue sur ATJ Beta
# From: noreply@atjbeta.local
# To: client@example.com
# ─────────────────────────────────
# Message du test...
```

### Twilio, SendGrid, etc.

```bash
# Toujours utiliser les clés TEST:

# ✅ Twilio TEST
TWILIO_ACCOUNT_SID=AC123456789test...

# ✅ SendGrid TEST API Key
SENDGRID_API_KEY=SG.testkey...

# ✅ Google Cloud TEST Project
GOOGLE_PROJECT_ID=my-project-test
```

---

## 🌐 PROTECTION 5: ISOLATION DÉPLOIEMENT

### ALLOWED_HOSTS

```bash
# .env.beta - Domaine BETA SEULEMENT
ALLOWED_HOSTS=beta.monprojet.com,localhost,127.0.0.1

# ✅ Cela signifie:
# - beta.monprojet.com ✅
# - staging.monprojet.com ❌
# - monprojet.com (production) ❌
# - api.monprojet.com ❌

# Si quelqu'un essaie d'accéder au mauvais domaine:
# 400 Bad Request
```

### CSRF_TRUSTED_ORIGINS

```bash
# Seulement les origines BETA
CSRF_TRUSTED_ORIGINS=https://beta.monprojet.com,http://localhost:8000

# Les requêtes POST depuis production seront rejetées
```

### SSL/HTTPS

```bash
# Développement local
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Production beta (HTTPS obligatoire)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000  # Force HTTPS 1 an
```

---

## 🔑 GESTION DES SECRETS

### .env.beta Structure

```bash
# ✅ À avoir dans .env.beta:
SECRET_KEY=django-insecure-unique-beta-key-64-chars-min
DEBUG=True
ALLOWED_HOSTS=beta.monprojet.com,localhost
DATABASE_NAME=db_beta.sqlite3
ENABLE_BASIC_AUTH=True
BASIC_AUTH_PASSWORD=very_secure_12345
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
MEDIA_ROOT=media_beta
```

### .env (Production)

```bash
# ⚠️  NE JAMAIS commiter .env sur git!
# À avoir dans production (serveur uniquement):
SECRET_KEY=django-insecure-unique-production-key-TRÈS-DIFFÉRENTE
DEBUG=False
ALLOWED_HOSTS=monprojet.com,www.monprojet.com
DATABASE_NAME=db.sqlite3
ENABLE_BASIC_AUTH=False
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
MEDIA_ROOT=media
```

### Git Configuration

```bash
# .gitignore - JAMAIS commiter les .env
.env
.env.beta
.env.*.local
secrets.txt
```

**Vérifier:**

```bash
# Confirmer qu'on n'a pas d'env secrets
git status
# Ne doit pas afficher .env ou .env.beta

# Vérifier l'historique
git log --all --full-history -- ".env.beta"
# Doit être vide
```

---

## ✅ CHECKLIST DE SÉCURITÉ

Avant de partager le site avec le client:

```bash
# Données
[ ] db.sqlite3 (production) intacte et non modifiée
[ ] db_beta.sqlite3 créée et isolée
[ ] media_beta/ dossier créé (uploads de test)
[ ] media/ production non affecté

# Configuration
[ ] .env.beta créé avec valeurs uniques
[ ] SECRET_KEY différente de production
[ ] STRIPE_SECRET_KEY commence par sk_test_
[ ] EMAIL_BACKEND = console (pas d'envoi réel)
[ ] DEBUG = True (mais peut être False)

# Sécurité d'Accès
[ ] ENABLE_BASIC_AUTH = True
[ ] BASIC_AUTH_PASSWORD changé (min 8 chars)
[ ] ALLOWED_HOSTS = domaine beta seulement
[ ] CSRF_TRUSTED_ORIGINS = origines beta seulement

# Code & Déploiement
[ ] settings_beta.py créé et configuré
[ ] core/middleware.py contient BasicAuthMiddleware
[ ] .gitignore contient .env.beta
[ ] Aucun secret hardcodé dans le code
[ ] Scripts déploiement testés localement

# Validations
[ ] python3 validate_security.py (tous OK)
[ ] python3 manage.py check --settings=atj_site.settings_beta (OK)
[ ] Site accessible localement sur http://localhost:8000
[ ] Basic Auth demande identifiants
[ ] Admin accessible via /admin/
[ ] Uploads médias vont dans media_beta/
```

---

## 🚨 SIGNAUX D'ALERTE

### Ne jamais faire ceci:

```python
❌ DANGEREUX: Utiliser la BD production
DATABASES['default']['NAME'] = 'db.sqlite3'  # Partage data avec production!

❌ DANGEREUX: Utiliser les médias production
MEDIA_ROOT = 'media'  # Les uploads de test touchent production!

❌ DANGEREUX: DEBUG = False (caché si erreur)
DEBUG = False  # Les erreurs ne s'affichent pas, difficile à déboguer

❌ DANGEREUX: Clés LIVE en beta
STRIPE_SECRET_KEY = 'sk_live_...'  # Charges réelles pendant les tests!

❌ DANGEREUX: Envoyer des vrais emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Les emails de test sont envoyés aux vrais clients!

❌ DANGEREUX: Commiter .env.beta
git add .env.beta  # Les secrets sont en public!

❌ DANGEREUX: ALLOWED_HOSTS = '*'
ALLOWED_HOSTS = ['*']  # N'importe quel domaine peut accéder!
```

---

## 🔄 ENTRETIEN & MONITORING

### Checks hebdomadaires

```bash
# Vérifier l'intégrité
python3 validate_security.py

# Vérifier les logs pour erreurs
tail -f logs/gunicorn_error.log

# Vérifier que production n'est pas affectée
ls -la db.sqlite3           # Taille/date inchangées?
du -sh media/               # Pas de nouveaux fichiers?

# Vérifier les permissions
ls -la .env.beta            # Seulement propriétaire peut lire?
```

### Rotation des secrets

```bash
# Tous les 90 jours:

# 1. Générer une nouvelle SECRET_KEY
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 2. Mettre à jour .env.beta
BASIC_AUTH_PASSWORD=new_very_secure_password_2024

# 3. Redéployer
bash deploy_beta.sh
sudo systemctl restart atj_beta
```

---

## 📞 QUESTIONS FRÉQUENTES

**Q: Les données de test du client resteront-elles visibles après le test?**

A: Oui, dans `db_beta.sqlite3` et `media_beta/`. Vous pouvez les garder, les archiver, ou les supprimer.

```bash
# Pour supprimer toutes les données de test:
rm db_beta.sqlite3
rm -rf media_beta/*
```

**Q: Puis-je utiliser une vraie BD PostgreSQL en beta?**

A: Oui! Modifiez simplement `settings_beta.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'atj_beta',
        'USER': 'postgres_beta',
        'PASSWORD': '...',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Q: Que faire si je me trompe et modifie la BD production?**

A: Utilisez le rollback:

```bash
./rollback.sh
# Restaure tout en 30 secondes
```

**Q: Puis-je donner accès au client en production (HTTPS)?**

A: Oui! Configurez simplement:

```bash
# .env.beta (production)
ALLOWED_HOSTS=beta.monprojet.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
BASIC_AUTH_PASSWORD=client_password_here
```

**Q: Comment monitorer les accès?**

A: Vérifiez les logs d'accès:

```bash
# Qui a accédé quand?
tail -f /var/log/nginx/atj_beta_access.log

# Y a-t-il eu des erreurs?
tail -f /var/log/nginx/atj_beta_error.log
tail -f /home/atjbeta/given/logs/gunicorn_error.log
```

---

## 🎓 RÉSUMÉ FINAL

La configuration beta fournie garantit:

✅ **Zéro impact** sur la production  
✅ **Isolation totale** des données  
✅ **Accès sécurisé** (Basic Auth)  
✅ **Services en mode TEST** (Stripe, Email)  
✅ **Rollback instantané** en cas de problème  
✅ **Facilité d'administration** pour le client  

**Vous pouvez lancer la beta en CONFIANCE!**
