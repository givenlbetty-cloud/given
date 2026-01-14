#!/usr/bin/env python3
"""
🔐 VALIDATEUR DE SÉCURITÉ BETA
Vérifie que l'environnement beta est correctement isolé et sécurisé
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_env_file():
    """Vérifier que .env.beta existe et est configuré"""
    print("\n🔐 VALIDATION DE .env.beta\n")
    
    if not Path('.env.beta').exists():
        print("❌ .env.beta manquant")
        print("   Créez-le: cp .env.beta.example .env.beta")
        return False
    
    load_dotenv('.env.beta')
    
    required_vars = {
        'SECRET_KEY': 'Clé secrète unique',
        'DEBUG': 'Mode debug (True/False)',
        'ALLOWED_HOSTS': 'Domaines autorisés',
        'DATABASE_NAME': 'Nom BD beta',
        'ENABLE_BASIC_AUTH': 'Basic Auth activé',
        'BASIC_AUTH_USERNAME': 'Utilisateur Basic Auth',
        'BASIC_AUTH_PASSWORD': 'Mot de passe Basic Auth',
        'MEDIA_ROOT': 'Dossier médias beta',
        'STRIPE_SECRET_KEY': 'Clé Stripe (doit être test)',
    }
    
    missing = []
    issues = []
    
    for var, description in required_vars.items():
        value = os.getenv(var, '').strip()
        
        if not value:
            missing.append(f"  ❌ {var} manquant")
            continue
        
        # Validations spécifiques
        if var == 'SECRET_KEY':
            if value.startswith('django-insecure') or len(value) < 50:
                issues.append(f"  ⚠️  SECRET_KEY trop court ou par défaut (min 50 chars)")
        
        if var == 'STRIPE_SECRET_KEY':
            if value.startswith('sk_live_'):
                issues.append(f"  🔴 ERREUR CRITIQUE: Clé PRODUCTION Stripe détectée!")
                issues.append(f"     Utilisez une clé TEST (sk_test_)")
            elif value.startswith('sk_test_'):
                print(f"  ✅ {var}: Clé TEST Stripe détectée (OK)")
                continue
        
        if var == 'DATABASE_NAME':
            if 'db_beta' not in value.lower():
                issues.append(f"  ⚠️  DATABASE_NAME devrait contenir 'db_beta' (actuellement: {value})")
            else:
                print(f"  ✅ {var}: {value} (BD isolée)")
        
        if var == 'MEDIA_ROOT':
            if 'media_beta' not in value.lower():
                issues.append(f"  ⚠️  MEDIA_ROOT devrait contenir 'media_beta' (actuellement: {value})")
            else:
                print(f"  ✅ {var}: {value} (Médias isolés)")
        
        if var == 'ALLOWED_HOSTS':
            hosts = value.split(',')
            if '*' in hosts:
                issues.append(f"  ⚠️  ALLOWED_HOSTS='*' détecté - Trop permissif!")
            else:
                print(f"  ✅ {var}: {hosts[0]} (+{len(hosts)-1} autres)")
        
        if var == 'DEBUG':
            if value == 'True':
                print(f"  ✅ {var}: True (Mode développement)")
            else:
                print(f"  ✅ {var}: False (Mode production)")
        
        if var == 'ENABLE_BASIC_AUTH':
            if value == 'True':
                print(f"  ✅ {var}: True (Accès protégé)")
            else:
                print(f"  ⚠️  {var}: False (Site public - non recommandé)")
        
        if var in ['BASIC_AUTH_USERNAME', 'BASIC_AUTH_PASSWORD']:
            pwd = os.getenv('BASIC_AUTH_PASSWORD', '')
            if len(pwd) < 8:
                issues.append(f"  ⚠️  Mot de passe Basic Auth trop court (min 8 chars)")
            elif pwd == 'change_this_secure_password_12345':
                issues.append(f"  🔴 Mot de passe Basic Auth par défaut!")
            else:
                print(f"  ✅ {var}: Configuré")
    
    if missing:
        print("\n❌ VARIABLES MANQUANTES:")
        for msg in missing:
            print(msg)
    
    if issues:
        print("\n⚠️  PROBLÈMES TROUVÉS:")
        for msg in issues:
            print(msg)
    
    return len(missing) == 0 and len(issues) == 0


def check_database_isolation():
    """Vérifier que la BD beta est isolée"""
    print("\n📊 VALIDATION ISOLATION BASE DE DONNÉES\n")
    
    db_beta = Path('db_beta.sqlite3')
    db_prod = Path('db.sqlite3')
    
    if not db_beta.exists():
        print(f"  ℹ️  db_beta.sqlite3 n'existe pas (sera créé au premier migration)")
    else:
        size = db_beta.stat().st_size
        print(f"  ✅ db_beta.sqlite3 existe ({size} bytes)")
    
    if db_prod.exists():
        size = db_prod.stat().st_size
        print(f"  ✅ db.sqlite3 (Production) existe ({size} bytes)")
        
        # Vérifier qu'elles sont différentes
        if db_beta.exists():
            if db_beta.stat().st_ino == db_prod.stat().st_ino:
                print(f"  🔴 ERREUR: Les deux BD pointent vers le même fichier!")
                return False
            else:
                print(f"  ✅ Les deux BD sont correctement isolées")
    
    return True


def check_media_isolation():
    """Vérifier que les médias sont isolés"""
    print("\n📁 VALIDATION ISOLATION MÉDIAS\n")
    
    media_beta = Path('media_beta')
    media_prod = Path('media')
    
    if not media_beta.exists():
        print(f"  ℹ️  Dossier media_beta n'existe pas (sera créé lors du déploiement)")
    else:
        print(f"  ✅ Dossier media_beta existe")
    
    if media_prod.exists():
        print(f"  ✅ Dossier media (Production) existe")
    
    # Vérifier qu'ils ne sont pas le même
    if media_beta.exists() and media_prod.exists():
        if media_beta.samefile(media_prod):
            print(f"  🔴 ERREUR: media_beta et media pointent vers le même dossier!")
            return False
        else:
            print(f"  ✅ Les dossiers médias sont correctement isolés")
    
    return True


def check_git_isolation():
    """Vérifier que .env.beta n'est pas dans git"""
    print("\n📚 VALIDATION ISOLATION GIT\n")
    
    try:
        with open('.gitignore', 'r') as f:
            content = f.read()
            if '.env.beta' in content:
                print(f"  ✅ .env.beta est dans .gitignore")
            else:
                print(f"  ⚠️  .env.beta n'est pas dans .gitignore")
                print(f"     Ajoutez cette ligne à .gitignore:")
                print(f"       echo '.env.beta' >> .gitignore")
    except FileNotFoundError:
        print(f"  ⚠️  .gitignore n'existe pas")
        return False
    
    return True


def check_middleware():
    """Vérifier que les middlewares beta sont configurés"""
    print("\n⚙️  VALIDATION MIDDLEWARE\n")
    
    middleware_file = Path('core/middleware.py')
    
    if not middleware_file.exists():
        print(f"  ❌ core/middleware.py n'existe pas")
        return False
    
    with open(middleware_file, 'r') as f:
        content = f.read()
        
        if 'BasicAuthMiddleware' in content:
            print(f"  ✅ BasicAuthMiddleware configuré")
        else:
            print(f"  ❌ BasicAuthMiddleware manquant")
            return False
        
        if 'BetaEnvironmentHeaderMiddleware' in content:
            print(f"  ✅ BetaEnvironmentHeaderMiddleware configuré")
        else:
            print(f"  ⚠️  BetaEnvironmentHeaderMiddleware manquant")
    
    return True


def check_settings_beta():
    """Vérifier que settings_beta.py existe"""
    print("\n⚙️  VALIDATION SETTINGS BETA\n")
    
    settings_file = Path('atj_site/settings_beta.py')
    
    if not settings_file.exists():
        print(f"  ❌ atj_site/settings_beta.py n'existe pas")
        return False
    
    print(f"  ✅ atj_site/settings_beta.py existe")
    
    with open(settings_file, 'r') as f:
        content = f.read()
        
        checks = {
            'settings_beta': 'Configuration beta',
            'BasicAuthMiddleware': 'Basic Auth',
            'BetaEnvironmentHeaderMiddleware': 'Headers beta',
            'db_beta': 'BD isolée',
            'media_beta': 'Médias isolés',
            'pk_test_': 'Stripe TEST mode check',
        }
        
        for check, desc in checks.items():
            if check in content:
                print(f"  ✅ {desc}: Configuré")
            elif check == 'pk_test_':
                # Stripe check est optionnel (peut être dans .env.beta)
                print(f"  ℹ️  {desc}: À vérifier dans .env.beta")
            else:
                print(f"  ⚠️  {desc}: Non configuré")
    
    return True


def main():
    print("\n" + "="*70)
    print("🔐 VALIDATEUR DE SÉCURITÉ - ENVIRONNEMENT BETA")
    print("="*70)
    
    checks = [
        ("Configuration .env.beta", check_env_file()),
        ("Isolation BD", check_database_isolation()),
        ("Isolation Médias", check_media_isolation()),
        ("Isolation Git", check_git_isolation()),
        ("Middleware", check_middleware()),
        ("Settings Beta", check_settings_beta()),
    ]
    
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DE SÉCURITÉ")
    print("="*70 + "\n")
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for name, result in checks:
        status = "✅ OK" if result else "❌ ÉCHEC"
        print(f"{status} - {name}")
    
    print("\n" + "="*70)
    
    if passed == total:
        print("✅ ENVIRONNEMENT BETA SÉCURISÉ - PRÊT POUR LE DÉPLOIEMENT!")
        print("\nProchaines étapes:")
        print("  1. bash deploy_beta.sh")
        print("  2. bash run_beta.sh")
        print("  3. Accédez à http://localhost:8000")
        print("     (Identifiants Basic Auth: beta_user / [votre mot de passe])")
        print("="*70 + "\n")
        return 0
    else:
        print(f"⚠️  PROBLÈMES TROUVÉS: {total - passed} vérifications échouées")
        print("\nCorrigez les erreurs avant de déployer.")
        print("="*70 + "\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
