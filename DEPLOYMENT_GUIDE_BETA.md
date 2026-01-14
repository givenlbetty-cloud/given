# 🚀 GUIDE COMPLET DE DÉPLOIEMENT BETA - ENVIRONNEMENT DE TEST CLIENT

**Dernière mise à jour:** Janvier 2026  
**Environnement:** Django 6.0.1 + Python 3.12  
**Isolation:** BD séparée, médias séparés, configuration dédiée  

---

## 📋 TABLE DES MATIÈRES

1. [Configuration Locale](#configuration-locale)
2. [Déploiement sur Render](#déploiement-sur-render)
3. [Déploiement sur Railway](#déploiement-sur-railway)
4. [Déploiement sur VPS Custom](#déploiement-sur-vps-custom)
5. [Sécurité & Protections](#sécurité--protections)
6. [Rollback & Récupération](#rollback--récupération)
7. [Monitoring](#monitoring)

---

## ⚙️ CONFIGURATION LOCALE

### Prérequis
```bash
# Python 3.10+
python3 --version

# pip
pip install --upgrade pip

# Git
git --version
```

### Installation
```bash
# 1. Cloner le projet
git clone https://github.com/givenlbetty-cloud/given.git
cd given

# 2. Créer l'environnement Python
python3 -m venv venv_beta
source venv_beta/bin/activate  # Linux/Mac
# OU
venv_beta\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
pip install python-dotenv  # Important pour charger .env.beta

# 4. Configurer l'environnement beta
cp .env.beta.example .env.beta

# 5. Éditer .env.beta avec vos valeurs
nano .env.beta  # Linux/Mac
# OU
notepad .env.beta  # Windows
```

### Configuration .env.beta

Remplissez les valeurs suivantes:

```bash
# Sécurité
SECRET_KEY=your-unique-random-key-here-64-chars-minimum
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,beta.monprojet.com

# Base de données
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db_beta.sqlite3

# Protection Basic Auth (RECOMMANDÉ)
ENABLE_BASIC_AUTH=True
BASIC_AUTH_USERNAME=beta_user
BASIC_AUTH_PASSWORD=very_secure_password_12345

# Médias séparés
MEDIA_ROOT=media_beta
MEDIA_URL=/media_beta/

# Email (Console = pas d'envoi réel)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Services tiers (TEST/SANDBOX UNIQUEMENT)
STRIPE_PUBLIC_KEY=pk_test_your_test_key
STRIPE_SECRET_KEY=sk_test_your_test_key
STRIPE_WEBHOOK_SECRET=whsec_test_your_webhook_key

# Domaine de test
CSRF_TRUSTED_ORIGINS=https://beta.monprojet.com,http://localhost:8000
```

### Déploiement Local

```bash
# 1. Charger l'environnement
export $(cat .env.beta | xargs)

# 2. Préparer l'environnement
bash deploy_beta.sh

# 3. Lancer le serveur
bash run_beta.sh

# 4. Accédez à http://localhost:8000
# Identifiants Basic Auth: beta_user / very_secure_password_12345
# Admin: admin_beta / beta_admin_password_123
```

---

## 🚀 DÉPLOIEMENT SUR RENDER

### Avantages
✅ Déploiement facile depuis GitHub  
✅ HTTPS automatique  
✅ Environnement isolé  
✅ Backing automatiques  

### Étapes

#### 1. Préparer le projet pour Render

```bash
# Ajouter requirements_beta.txt spécifique
cat requirements.txt > requirements_beta.txt
echo "gunicorn==21.2.0" >> requirements_beta.txt
echo "python-dotenv==1.0.0" >> requirements_beta.txt

# Créer un fichier build.sh
cat > build.sh << 'EOF'
#!/bin/bash
set -e

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements_beta.txt

# Migrations
python3 manage.py migrate --settings=atj_site.settings_beta

# Collecte static
python3 manage.py collectstatic --noinput --settings=atj_site.settings_beta

echo "✅ Build terminé"
EOF

chmod +x build.sh

# Committer
git add .
git commit -m "feat: beta deployment configuration"
git push origin main
```

#### 2. Créer un service sur Render

1. Aller à [render.com](https://render.com)
2. Cliquer "New +"
3. Sélectionner "Web Service"
4. Connecter votre repo GitHub
5. Remplir les champs:

```
Name: atj-site-beta
Environment: Python 3.12
Build Command: bash build.sh
Start Command: gunicorn atj_site.wsgi:application \
  --bind 0.0.0.0:8000 \
  --settings atj_site.settings_beta \
  --workers 4 \
  --timeout 60
```

#### 3. Ajouter les variables d'environnement

Dans Render Dashboard → Environment:

```
SECRET_KEY=your-unique-random-key
DEBUG=True
ALLOWED_HOSTS=atj-site-beta.onrender.com,localhost
DATABASE_NAME=db_beta.sqlite3
ENABLE_BASIC_AUTH=True
BASIC_AUTH_USERNAME=beta_user
BASIC_AUTH_PASSWORD=secure_password_here
MEDIA_ROOT=media_beta
MEDIA_URL=/media_beta/
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### 4. Déployer

```bash
# Push sur main déclenche le déploiement automatique
git push origin main

# Ou utiliser le dashboard Render pour redéployer manuellement
```

#### 5. Accéder au site

- URL: `https://atj-site-beta.onrender.com`
- Admin: `https://atj-site-beta.onrender.com/admin/`
- Identifiants Basic Auth: `beta_user` / `secure_password_here`
- Admin: `admin_beta` / `beta_admin_password_123`

---

## 🚀 DÉPLOIEMENT SUR RAILWAY

### Avantages
✅ Interface intuitive  
✅ BD PostgreSQL inclus (optionnel)  
✅ Accès SSH possible  
✅ Logs en temps réel  

### Étapes

#### 1. Créer un compte Railway

1. Aller à [railway.app](https://railway.app)
2. Sign up avec GitHub
3. New Project

#### 2. Connecter GitHub

```bash
# Railway détecte automatiquement Django
# Il crée les services nécessaires
```

#### 3. Configuration Railway

Ajouter un `railway.json`:

```json
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "never",
    "restartPolicyMaxRetries": 0
  }
}
```

#### 4. Dockerfile pour Railway

Créer `Dockerfile.beta`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Migrations et static files
RUN python3 manage.py migrate --settings=atj_site.settings_beta --noinput
RUN python3 manage.py collectstatic --noinput --settings=atj_site.settings_beta

# Exposer le port
EXPOSE 8000

# Démarrer Gunicorn
CMD ["gunicorn", "atj_site.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--settings", "atj_site.settings_beta", \
     "--workers", "4", \
     "--timeout", "60"]
```

#### 5. Variables d'environnement Railway

Dans Railway Dashboard → Project → Variables:

```
SECRET_KEY=your-unique-key
DEBUG=True
ALLOWED_HOSTS=*.railway.app,localhost
ENABLE_BASIC_AUTH=True
BASIC_AUTH_USERNAME=beta_user
BASIC_AUTH_PASSWORD=secure_password
```

---

## 🚀 DÉPLOIEMENT SUR VPS CUSTOM

### Prérequis (Linux Ubuntu 22.04+)

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer les dépendances
sudo apt install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    git \
    nginx \
    supervisor \
    postgresql

# Installer Node.js (optionnel, pour assets)
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### Installation sur VPS

```bash
# 1. Créer l'utilisateur et le répertoire
sudo useradd -m -d /home/atjbeta atjbeta
sudo su - atjbeta

# 2. Cloner le projet
cd /home/atjbeta
git clone https://github.com/givenlbetty-cloud/given.git
cd given

# 3. Créer l'environnement virtuel
python3.12 -m venv venv_beta
source venv_beta/bin/activate

# 4. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn supervisor

# 5. Créer .env.beta
cp .env.beta.example .env.beta
# Éditer avec vos valeurs
nano .env.beta

# 6. Préparer
bash deploy_beta.sh

# 7. Vérifier
python3 manage.py check --settings=atj_site.settings_beta
```

### Configuration Gunicorn

Créer `/home/atjbeta/gunicorn_beta.py`:

```python
import multiprocessing

bind = "unix:/home/atjbeta/given/gunicorn_beta.sock"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 60
accesslog = "/home/atjbeta/given/logs/gunicorn_access.log"
errorlog = "/home/atjbeta/given/logs/gunicorn_error.log"
loglevel = "info"

# Charger settings_beta
raw_env = [
    "DJANGO_SETTINGS_MODULE=atj_site.settings_beta"
]
```

### Configuration Supervisor

Créer `/etc/supervisor/conf.d/atj_beta.conf`:

```ini
[program:atj_beta]
directory=/home/atjbeta/given
command=/home/atjbeta/given/venv_beta/bin/gunicorn \
    atj_site.wsgi:application \
    -c gunicorn_beta.py

user=atjbeta
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/atjbeta/given/logs/supervisor.log
environment=DJANGO_SETTINGS_MODULE=atj_site.settings_beta
```

Activez:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start atj_beta
```

### Configuration Nginx

Créer `/etc/nginx/sites-available/atj_beta`:

```nginx
server {
    listen 80;
    server_name beta.monprojet.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name beta.monprojet.com;

    # Certificats SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/beta.monprojet.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/beta.monprojet.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Gzip
    gzip on;
    gzip_types text/plain text/css text/javascript application/json;

    # Statiques
    location /static/ {
        alias /home/atjbeta/given/staticfiles_beta/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Médias
    location /media_beta/ {
        alias /home/atjbeta/given/media_beta/;
        expires 7d;
    }

    # Proxy vers Gunicorn
    location / {
        proxy_pass http://unix:/home/atjbeta/given/gunicorn_beta.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

Activez:
```bash
sudo ln -s /etc/nginx/sites-available/atj_beta /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Certificat SSL (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d beta.monprojet.com
```

---

## 🔒 SÉCURITÉ & PROTECTIONS

### 1. Basic Auth (Middleware)

Automatiquement activé si `ENABLE_BASIC_AUTH=True` dans `.env.beta`:

```python
# Demande identifiants avant d'accéder au site
BASIC_AUTH_USERNAME=beta_user
BASIC_AUTH_PASSWORD=secure_password_12345
```

### 2. Isolation Base de Données

```bash
# Production
db.sqlite3

# Beta
db_beta.sqlite3

# Les données de test ne touchent JAMAIS la production
```

### 3. Isolation Médias

```bash
# Production
media/

# Beta
media_beta/

# Les uploads de test sont séparés
```

### 4. Secrets & Clés API

- ✅ SECRET_KEY différente
- ✅ Stripe: Clés TEST uniquement (pk_test_, sk_test_)
- ✅ Email: Console backend (pas d'envoi réel)
- ✅ Jamais de .env.beta sur git (ajouter au .gitignore)

### 5. ALLOWED_HOSTS & CSRF

```bash
# Seulement le domaine beta
ALLOWED_HOSTS=beta.monprojet.com,localhost,127.0.0.1

CSRF_TRUSTED_ORIGINS=https://beta.monprojet.com,http://localhost:8000
```

### 6. SSL/HTTPS en Production

```bash
# En .env.beta (déploiement final):
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

---

## 🔄 ROLLBACK & RÉCUPÉRATION

### En cas de problème

#### Option 1: Utiliser le script de rollback automatique

```bash
chmod +x rollback.sh
./rollback.sh

# Cela:
# 1. Arrête le serveur
# 2. Revient à main
# 3. Restaure la BD originale
# 4. Relance le serveur
```

#### Option 2: Rollback manuel

```bash
# 1. Arrêter le serveur
sudo systemctl stop atj_beta
# OU
sudo supervisorctl stop atj_beta

# 2. Revenir à main
git checkout main

# 3. Restaurer la BD
rm db_beta.sqlite3
# Recharger depuis backup ou réinitialiser

# 4. Relancer
sudo systemctl start atj_beta
# OU
sudo supervisorctl start atj_beta
```

#### Option 3: Restaurer depuis backup

```bash
# Si vous avez un backup:
cp db_beta.sqlite3.backup db_beta.sqlite3

# Puis redémarrer l'app
```

---

## 📊 MONITORING

### Vérifier l'état du service

```bash
# Status du service
sudo systemctl status atj_beta
# OU
sudo supervisorctl status atj_beta

# Voir les logs
tail -f /home/atjbeta/given/logs/gunicorn_error.log
tail -f /home/atjbeta/given/logs/supervisor.log

# Nombre de requêtes
tail -f /home/atjbeta/given/logs/gunicorn_access.log
```

### Metrics simples

```bash
# Espace disque utilisé
du -sh /home/atjbeta/given/media_beta
du -sh /home/atjbeta/given/db_beta.sqlite3

# Processus actifs
ps aux | grep gunicorn
ps aux | grep supervisor

# Ports écoutant
sudo netstat -tulpn | grep 8000
```

### Alerts recommandées

- 🔴 Espace disque < 5%
- 🔴 Erreurs dans logs (ERROR, CRITICAL)
- 🔴 Service arrêté inopinément
- 🟡 Temps de réponse > 5 secondes
- 🟡 Mémoire > 80% de la limite

---

## ✅ CHECKLIST DÉPLOIEMENT

```bash
# Avant le déploiement
[ ] Configuration .env.beta complète
[ ] SECRET_KEY différente de production
[ ] ALLOWED_HOSTS correctement configuré
[ ] Basic Auth activé (ENABLE_BASIC_AUTH=True)
[ ] Stripe: Clés TEST confirmées
[ ] Email backend: Console backend configuré
[ ] SSL/HTTPS: Certificat valide
[ ] Backups: BD sauvegardée localement
[ ] Tests: Tous les endpoints testés

# Après le déploiement
[ ] Site accessible via domaine
[ ] Basic Auth: Fonctionne
[ ] Login/Signup: Fonctionne
[ ] Admin: Accessible et fonctionnel
[ ] Uploads médias: Fonctionnent
[ ] Emails: S'affichent en console (pas d'envoi)
[ ] Logs: Monitorer pour erreurs
[ ] Performance: Acceptables
```

---

## 📞 SUPPORT & TROUBLESHOOTING

### Le site ne démarre pas

```bash
# Vérifier la configuration
python3 manage.py check --settings=atj_site.settings_beta

# Vérifier les logs
cat logs/gunicorn_error.log
cat logs/supervisor.log
```

### Erreur: "Module not found"

```bash
# Réinstaller les dépendances
source venv_beta/bin/activate
pip install -r requirements.txt
```

### Basic Auth ne marche pas

```bash
# Vérifier .env.beta
cat .env.beta | grep ENABLE_BASIC_AUTH

# Doit être:
# ENABLE_BASIC_AUTH=True
# BASIC_AUTH_USERNAME=beta_user
# BASIC_AUTH_PASSWORD=your_password
```

### BD de production est affectée

```bash
# UTILISER LE ROLLBACK:
./rollback.sh

# Cette commande restaure tout en 30 secondes
```

---

## 📝 NOTES FINALES

✅ **Isolation totale**: BD, médias, config séparés  
✅ **Sécurité maximale**: Basic Auth, SSL/HTTPS, Stripe TEST  
✅ **Facile à maintenir**: Scripts d'automatisation fournis  
✅ **Rollback rapide**: < 30 secondes en cas de problème  
✅ **Production protégée**: main branch inchangée  

**La version beta peut être lancée en confiance pour le test client!**
