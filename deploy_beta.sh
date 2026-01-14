#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════
# 🚀 SCRIPT DE DÉPLOIEMENT BETA - Étape 1
# Prépare l'environnement, migre la BD et collecte les fichiers statiques
# ═══════════════════════════════════════════════════════════════════════

set -e  # Arrêter à la première erreur

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 DÉPLOIEMENT ENVIRONNEMENT BETA                        ║"
echo "║  Étape 1: Préparation et Migrations                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# 1️⃣  Vérifier les fichiers nécessaires
# ═══════════════════════════════════════════════════════════════════════

echo "1️⃣  Vérification des fichiers..."
echo ""

if [ ! -f ".env.beta" ]; then
    echo "❌ ERREUR: Fichier .env.beta manquant!"
    echo ""
    echo "Créez-le avec:"
    echo "  cp .env.beta.example .env.beta"
    echo "  # puis éditez .env.beta avec vos valeurs"
    exit 1
fi

if [ ! -f "manage.py" ]; then
    echo "❌ ERREUR: manage.py non trouvé"
    echo "   Exécutez ce script depuis la racine du projet Django"
    exit 1
fi

echo "✅ .env.beta trouvé"
echo "✅ manage.py trouvé"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# 2️⃣  Charger les variables d'environnement
# ═══════════════════════════════════════════════════════════════════════

echo "2️⃣  Chargement des variables d'environnement..."
export $(cat .env.beta | xargs)
echo "✅ Variables chargées"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# 3️⃣  Créer les dossiers nécessaires
# ═══════════════════════════════════════════════════════════════════════

echo "3️⃣  Création des dossiers..."
mkdir -p media_beta
mkdir -p staticfiles_beta
mkdir -p logs
echo "✅ Dossiers créés: media_beta, staticfiles_beta, logs"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# 4️⃣  Migrations Base de Données
# ═══════════════════════════════════════════════════════════════════════

echo "4️⃣  Migrations de la base de données..."
echo "   Database: $(pwd)/${DATABASE_NAME}"
echo ""

python3 manage.py migrate --settings=atj_site.settings_beta

echo ""
echo "✅ Base de données migrée"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# 5️⃣  Collecte des fichiers statiques
# ═══════════════════════════════════════════════════════════════════════

echo "5️⃣  Collecte des fichiers statiques..."
echo ""

python3 manage.py collectstatic --noinput --settings=atj_site.settings_beta

echo ""
echo "✅ Fichiers statiques collectés"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# 6️⃣  Vérification du projet
# ═══════════════════════════════════════════════════════════════════════

echo "6️⃣  Vérification de la configuration Django..."
echo ""

python3 manage.py check --settings=atj_site.settings_beta

echo ""
echo "✅ Configuration validée"
echo ""

# ═══════════════════════════════════════════════════════════════════════
# 7️⃣  Créer un admin de test (optionnel)
# ═══════════════════════════════════════════════════════════════════════

echo "7️⃣  Création d'un compte administrateur de test..."
echo ""

# Vérifier s'il existe déjà un admin
if ! python3 manage.py shell --settings=atj_site.settings_beta << END
from django.contrib.auth import get_user_model
User = get_user_model()
print('EXISTS' if User.objects.filter(username='admin_beta').exists() else 'NOT_EXISTS')
END
then
    echo "Création du compte admin..."
    python3 manage.py shell --settings=atj_site.settings_beta << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin_beta').exists():
    admin = User.objects.create_superuser(
        username='admin_beta',
        email='admin@beta.local',
        password='beta_admin_password_123',
        first_name='Admin',
        last_name='Beta'
    )
    print(f"✅ Compte admin créé: admin_beta / beta_admin_password_123")
else:
    print("✅ Compte admin 'admin_beta' existe déjà")
END
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════
# ✅ RÉSUMÉ DU DÉPLOIEMENT
# ═══════════════════════════════════════════════════════════════════════

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ PRÉPARATION BETA TERMINÉE                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Résumé:"
echo "  ✅ Variables d'environnement chargées"
echo "  ✅ Dossiers créés (media_beta, staticfiles_beta)"
echo "  ✅ Base de données migrée (${DATABASE_NAME})"
echo "  ✅ Fichiers statiques collectés"
echo "  ✅ Configuration validée"
echo "  ✅ Compte admin créé (si non existant)"
echo ""
echo "🚀 Prochaine étape: Lancer le serveur"
echo ""
echo "  En développement:"
echo "    python3 manage.py runserver --settings=atj_site.settings_beta"
echo ""
echo "  En production (avec Gunicorn):"
echo "    gunicorn atj_site.wsgi:application --settings=atj_site.settings_beta"
echo ""
echo "📌 Informations de connexion admin:"
echo "    URL: http://localhost:8000/admin/ (ou votre domaine beta)"
echo "    Username: admin_beta"
echo "    Password: beta_admin_password_123"
echo "    ⚠️  CHANGEZ ce mot de passe après première connexion!"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
