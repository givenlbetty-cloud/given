import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
django.setup()

from formations.models import Programme, Session, Chapitre, Lecon

def run():
    print("Populating LMS Content...")

    # 1. Create or Get Programs
    p1, created = Programme.objects.get_or_create(
        titre="Maîtriser l'Art Oratoire",
        defaults={
            "categorie": "art_oratoire",
            "type_formation": "hybrid",
            "description": "Devenez un orateur confiant et charismatique. Cette formation couvre la rhétorique, le langage corporel et la gestion du stress.",
            "prix": 15000.00,
            "est_publie": True
        }
    )
    if created:
        print(f"Created Programme: {p1.titre}")
    else:
        print(f"Found Programme: {p1.titre}")

    p2, created = Programme.objects.get_or_create(
        titre="Leadership & Management",
        defaults={
            "categorie": "leadership",
            "type_formation": "online",
            "description": "Apprenez à diriger des équipes avec succès. Stratégies de motivation, délégation et résolution de conflits.",
            "prix": 25000.00,
            "est_publie": True
        }
    )
    if created:
        print(f"Created Programme: {p2.titre}")

    # 2. Create Sessions
    # Session for Art Oratoire (Hybrid)
    s1, created = Session.objects.get_or_create(
        programme=p1,
        date_debut=date.today() + timedelta(days=7),
        defaults={
            "date_fin": date.today() + timedelta(days=37),
            "lieu": "Campus ATJ, Riviera",
            "places_disponibles": 20
        }
    )
    
    # Session for Leadership (Online - Permanent)
    s2, created = Session.objects.get_or_create(
        programme=p2,
        est_permanente=True,
        defaults={
            "lieu": "En Ligne",
            "places_disponibles": 999
        }
    )

    # 3. Create Chapters and Lessons for Art Oratoire
    chapters_data = [
        {
            "titre": "Introduction à la Rhétorique",
            "lessons": [
                {"titre": "Bienvenue dans ce cours", "duree": 5, "gratuit": True, "video": "https://www.youtube.com/embed/dQw4w9WgXcQ"}, # Placeholder
                {"titre": "Les 3 piliers de la persuasion", "duree": 15, "gratuit": False, "video": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
                {"titre": "Analyser son auditoire", "duree": 12, "gratuit": False, "video": ""}
            ]
        },
        {
            "titre": "Communication Non-Verbale",
            "lessons": [
                {"titre": "La posture de l'orateur", "duree": 10, "gratuit": False, "video": ""},
                {"titre": "Gestuelle et regards", "duree": 20, "gratuit": False, "video": ""},
            ]
        },
        {
            "titre": "Structurer son discours",
            "lessons": [
                {"titre": "L'accroche (Exorde)", "duree": 8, "gratuit": False, "video": ""},
                {"titre": "Le développement", "duree": 25, "gratuit": False, "video": ""},
                {"titre": "La conclusion impactante (Péroraison)", "duree": 10, "gratuit": False, "video": ""}
            ]
        }
    ]

    for i, chap_data in enumerate(chapters_data):
        chap, c_created = Chapitre.objects.get_or_create(
            programme=p1,
            titre=chap_data["titre"],
            defaults={"ordre": i + 1}
        )
        
        for j, lesson_data in enumerate(chap_data["lessons"]):
            Lecon.objects.get_or_create(
                chapitre=chap,
                titre=lesson_data["titre"],
                defaults={
                    "ordre": j + 1,
                    "duree_minutes": lesson_data["duree"],
                    "est_gratuit": lesson_data["gratuit"],
                    "video_url": lesson_data["video"],
                    "contenu": f"<p>Contenu simulé pour la leçon <strong>{lesson_data['titre']}</strong>.</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>"
                }
            )

    print(f"Populated {p1.titre} with content.")

    # 4. Create Chapters for Leadership (Simpler)
    l_chap1, _ = Chapitre.objects.get_or_create(programme=p2, titre="Définir son style de Leadership", defaults={"ordre": 1})
    Lecon.objects.get_or_create(chapitre=l_chap1, titre="Vision vs Gestion", defaults={"ordre": 1, "duree_minutes": 15, "contenu": "<p>Le leader inspire, le manager gère.</p>"})
    Lecon.objects.get_or_create(chapitre=l_chap1, titre="Styles de leadership", defaults={"ordre": 2, "duree_minutes": 20, "contenu": "<p>Autocratique, Démocratique, Laissez-faire...</p>"})

    print(f"Populated {p2.titre} with content.")
    print("Done.")

if __name__ == '__main__':
    run()
