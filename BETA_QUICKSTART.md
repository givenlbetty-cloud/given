# 🚀 ENVIRONNEMENT BETA - DÉMARRAGE RAPIDE

Configuration sécurisée et isolée pour tester votre projet Django avec le client.

---

## ⚡ 5 MINUTES POUR LANCER LA BETA

### Étape 1: Préparer l'environnement (1 min)

```bash
# Créer le fichier de configuration beta
cp .env.beta.example .env.beta

# Éditer avec vos valeurs
nano .env.beta  # Ou votre éditeur préféré

# ⚠️  IMPORTANT:
# - Changer SECRET_KEY (générateur: python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
# - Changer BASIC_AUTH_PASSWORD (min 8 caractères)
# - Vérifier que STRIPE_SECRET_KEY commence par sk_test_ (jamais sk_live_)
```

### Étape 2: Valider la sécurité (1 min)

```bash
# Vérifier que tout est configuré correctement
python3 validate_security.py

# Doit afficher: ✅ ENVIRONNEMENT BETA SÉCURISÉ - PRÊT POUR LE DÉPLOIEMENT!
```

### Étape 3: Déployer (2 min)

```bash
# Préparer BD, médias, fichiers statiques
bash deploy_beta.sh

# Cela va:
# ✅ Vérifier les fichiers nécessaires
# ✅ Créer les dossiers (media_beta, staticfiles_beta)
# ✅ Migrer la BD (db_beta.sqlite3)
# ✅ Collecter les fichiers statiques
# ✅ Créer un compte admin (admin_beta / beta_admin_password_123)
```

### Étape 4: Lancer le serveur (1 min)

```bash
# Démarrer en mode développement
bash run_beta.sh

# OU mode production avec gunicorn
pip install gunicorn
gunicorn atj_site.wsgi:application \
    --bind 0.0.0.0:8000 \
    --settings atj_site.settings_beta
```

### Étape 5: Accéder au site (instant)

```
🌐 http://localhost:8000/

🔐 Identifiants Basic Auth:
   Username: beta_user
   Password: [celui que vous avez configuré dans .env.beta]

🔑 Admin Panel:
   URL: http://localhost:8000/admin/
   Username: admin_beta
   Password: beta_admin_password_123
   ⚠️  Changez ce mot de passe après première connexion!
```

---

## 📁 FICHIERS CRÉÉS

| Fichier | Rôle |
|---------|------|
| `.env.beta` | Variables d'environnement du projet beta |
| `settings_beta.py` | Configuration Django isolée |
| `core/middleware.py` | Authentification Basic Auth + Headers |
| `deploy_beta.sh` | Script de préparation de l'environnement |
| `run_beta.sh` | Script pour lancer le serveur |
| `validate_security.py` | Validateur de sécurité |
| `DEPLOYMENT_GUIDE_BETA.md` | Guide complet de déploiement (Render, Railway, VPS) |
| `SECURITY_GUIDE_BETA.md` | Guide détaillé de sécurité |
| `db_beta.sqlite3` | Base de données isolée (créée après deploy) |
| `media_beta/` | Dossier des médias de test (créé après deploy) |
| `staticfiles_beta/` | Fichiers statiques compilés (créé après deploy) |

---

## 🔐 PROTECTIONS ACTIVES

### 1. **Basic Auth** (Accès protégé par mot de passe)
   - Demande d'identifiants avant d'accéder au site
   - Middleware: `core/middleware.py::BasicAuthMiddleware`

### 2. **Isolation BD**
   - Production: `db.sqlite3`
   - Beta: `db_beta.sqlite3`
   - Aucun partage de données

### 3. **Isolation Médias**
   - Production: `media/`
   - Beta: `media_beta/`
   - Les uploads de test ne touchent pas la production

### 4. **Configuration Dédiée**
   - Production: `settings.py`
   - Beta: `settings_beta.py`
   - Variables d'env: `.env.beta` (jamais commité)

### 5. **Services Tiers en Mode TEST**
   - Stripe: Clés TEST uniquement (pk_test_, sk_test_)
   - Email: Console backend (pas d'envoi réel)
   - Jamais de clés LIVE (sk_live_) en beta

### 6. **Domaine Isolé**
   - `ALLOWED_HOSTS=beta.monprojet.com,localhost`
   - Les autres domaines sont rejetés (400 Bad Request)

---

## 🛠️ COMMANDES COURANTES

```bash
# Voir le statut du serveur
ps aux | grep runserver
ps aux | grep gunicorn

# Voir les logs
tail -f logs/gunicorn_error.log

# Accéder à la console Django
python3 manage.py shell --settings=atj_site.settings_beta

# Créer un nouveau superuser
python3 manage.py createsuperuser --settings=atj_site.settings_beta

# Exécuter les migrations
python3 manage.py migrate --settings=atj_site.settings_beta

# Collecter les fichiers statiques
python3 manage.py collectstatic --noinput --settings=atj_site.settings_beta

# Vérifier la configuration
python3 manage.py check --settings=atj_site.settings_beta

# Rollback en cas d'urgence
bash rollback.sh
```

---

## 🚀 DÉPLOIEMENT EN PRODUCTION (RENDER, RAILWAY, VPS)

Voir [DEPLOYMENT_GUIDE_BETA.md](DEPLOYMENT_GUIDE_BETA.md) pour:

- ✅ Render (le plus facile)
- ✅ Railway (interface intuitive)
- ✅ VPS Custom (Linux + Nginx + Supervisor)
- ✅ Configuration SSL/HTTPS
- ✅ Monitoring et logs

---

## ⚠️ EN CAS DE PROBLÈME

### Le site ne démarre pas

```bash
# Vérifier la configuration
python3 manage.py check --settings=atj_site.settings_beta

# Lire les logs
cat logs/gunicorn_error.log
```

### Erreur: "Module not found"

```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur: "address already in use"

```bash
# Le port 8000 est déjà utilisé
# Trouver le processus
lsof -i :8000

# Arrêter le processus
kill -9 <PID>

# Relancer
bash run_beta.sh
```

### La BD production est affectée!

```bash
# UTILISER LE ROLLBACK (< 30 secondes):
bash rollback.sh
```

---

## 📋 CHECKLIST PRÉ-DÉPLOIEMENT

Avant de partager avec le client:

```bash
✅ cp .env.beta.example .env.beta
✅ Éditer .env.beta avec vos valeurs
✅ python3 validate_security.py (tous OK)
✅ bash deploy_beta.sh (sans erreurs)
✅ bash run_beta.sh (serveur démarre)
✅ Accès à http://localhost:8000 (après Basic Auth)
✅ Admin fonctionne (/admin/)
✅ Uploads médias vont dans media_beta/
✅ Stripe: clés TEST (sk_test_)
✅ Email: mode console (pas d'envoi)
✅ db.sqlite3 intacte (production non affectée)
```

---

## 📞 SUPPORT

Pour des questions sur:

- **Configuration & Installation**: Voir [DEPLOYMENT_GUIDE_BETA.md](DEPLOYMENT_GUIDE_BETA.md)
- **Sécurité & Bonnes Pratiques**: Voir [SECURITY_GUIDE_BETA.md](SECURITY_GUIDE_BETA.md)
- **Dépannage**: Voir section "En cas de problème" ci-dessus

---

## 🎯 RÉSUMÉ

✅ **Configuration complète** fournie  
✅ **Isolation totale** production/beta  
✅ **Sécurité renforcée** (Basic Auth, BD séparée)  
✅ **Scripts automatisés** (deploy, run, validate)  
✅ **Rollback instantané** (< 30 secondes)  
✅ **Guide complet** pour déploiement (Render, Railway, VPS)  

**Vous êtes prêt à lancer la beta en confiance!** 🚀
