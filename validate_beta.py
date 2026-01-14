#!/usr/bin/env python3
"""
🔍 VALIDATION RAPIDE AVANT BETA
Vérifie que tout est prêt pour lancer la beta
"""

import os
import sys
import subprocess
from pathlib import Path

def check_git():
    """Vérifier le statut git"""
    try:
        result = subprocess.run(['git', 'branch'], capture_output=True, text=True, cwd='/workspaces/given')
        if 'beta-test' in result.stdout:
            print("✅ Git: Branch beta-test existe")
            return True
        else:
            print("❌ Git: Branch beta-test manquante")
            return False
    except Exception as e:
        print(f"❌ Git Error: {e}")
        return False

def check_database():
    """Vérifier les backups de BD"""
    files = {
        'db.sqlite3': False,
        'db.sqlite3.backup': False,
        'db.beta.sqlite3': False,
    }
    
    for fname in files:
        path = f'/workspaces/given/{fname}'
        if os.path.exists(path):
            size = os.path.getsize(path)
            files[fname] = size > 100000  # Plus que 100KB
            if files[fname]:
                print(f"✅ BD: {fname} ({size} bytes)")
            else:
                print(f"❌ BD: {fname} trop petit!")
        else:
            print(f"❌ BD: {fname} manquant!")
    
    return all(files.values())

def check_python():
    """Vérifier la syntaxe Python"""
    try:
        result = subprocess.run([
            'python3', 'manage.py', 'check'
        ], capture_output=True, text=True, cwd='/workspaces/given')
        
        if 'no issues' in result.stdout:
            print("✅ Python: Pas d'erreurs (manage.py check)")
            return True
        else:
            print(f"❌ Python: Erreurs trouvées\n{result.stdout}")
            return False
    except Exception as e:
        print(f"❌ Python Error: {e}")
        return False

def check_templates():
    """Vérifier les templates"""
    template_dir = Path('/workspaces/given/templates')
    if template_dir.exists():
        html_files = list(template_dir.glob('**/*.html'))
        print(f"✅ Templates: {len(html_files)} fichiers HTML trouvés")
        return len(html_files) > 5
    else:
        print("❌ Templates: répertoire manquant")
        return False

def check_static():
    """Vérifier les static files"""
    static_dir = Path('/workspaces/given/static')
    if static_dir.exists():
        files = list(static_dir.glob('**/*'))
        print(f"✅ Static: {len([f for f in files if f.is_file()])} fichiers trouvés")
        return True
    else:
        print("❌ Static: répertoire manquant")
        return False

def main():
    print("\n" + "="*60)
    print("🔍 VALIDATION BETA - PRÉ-DÉPLOIEMENT")
    print("="*60 + "\n")
    
    checks = [
        ("Git", check_git()),
        ("Database", check_database()),
        ("Python", check_python()),
        ("Templates", check_templates()),
        ("Static Files", check_static()),
    ]
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for name, result in checks:
        status = "✅ OK" if result else "❌ ÉCHEC"
        print(f"{status} - {name}")
    
    print("\n" + "="*60)
    if passed == total:
        print(f"✅ PRÊT POUR BETA! ({passed}/{total} vérifications réussies)")
        print("\nCommande pour lancer:")
        print("  python3 manage.py runserver 0.0.0.0:8000")
        print("\nEn cas de problème:")
        print("  ./rollback.sh")
        print("="*60 + "\n")
        return 0
    else:
        print(f"⚠️  PROBLÈMES TROUVÉS! ({passed}/{total} vérifications réussies)")
        print("\nCorrigez les erreurs avant de lancer la beta.")
        print("="*60 + "\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
