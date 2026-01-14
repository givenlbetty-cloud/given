import os
import django
from django.core.files.base import ContentFile
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
django.setup()

from library.models import Livre

def run():
    print("Populating Library...")

    books_data = [
        {
            "titre": "Guide du Leadership Moderne",
            "auteur": "Jean Dupont",
            "description": "Un guide complet pour devenir un leader inspirant dans le monde d'aujourd'hui. Couvre la communication, la gestion d'équipe et la prise de décision.",
            "prix": 0.00,  # Gratuit
        },
        {
            "titre": "Introduction à l'IA",
            "auteur": "Marie Curie (IA Edition)",
            "description": "Comprendre les bases de l'intelligence artificielle, du Machine Learning au Deep Learning, sans prérequis mathématiques complexes.",
            "prix": 19.99,
        },
        {
            "titre": "Le Marketing Digital pour les Nuls",
            "auteur": "Sophie Martin",
            "description": "Tout savoir sur le SEO, le SEA, les réseaux sociaux et l'emailing pour booster votre activité en ligne.",
            "prix": 29.50,
        },
        {
            "titre": "Réussir son Entretien d'Embauche",
            "auteur": "Paul Expert",
            "description": "Les secrets pour convaincre les recruteurs, gérer son stress et négocier son salaire.",
            "prix": 0.00,
        },
        {
            "titre": "Python Avancé",
            "auteur": "Guido van Rossum (Fan)",
            "description": "Techniques avancées de programmation en Python : décorateurs, générateurs, métaclasses et concurrence.",
            "prix": 45.00,
        },
        {
            "titre": "L'Art de la Négociation",
            "auteur": "Chris Voss (Inspiré)",
            "description": "Apprenez à ne jamais couper la poire en deux. Techniques de négociation éprouvées par le FBI.",
            "prix": 15.00,
        }
    ]

    # Create dummy PDF content
    dummy_content = b"Ceci est le contenu simule du livre. Il ne contient pas grand chose mais il permet de tester le telechargement."

    for book in books_data:
        livre, created = Livre.objects.get_or_create(
            titre=book["titre"],
            defaults={
                "auteur": book["auteur"],
                "description": book["description"],
                "prix": book["prix"],
            }
        )
        
        if created:
            # Add a dummy file
            livre.fichier.save(f"{book['titre'].replace(' ', '_').lower()}.txt", ContentFile(dummy_content))
            livre.save()
            print(f"Livre créé : {livre.titre} ({'Gratuit' if livre.is_free() else f'{livre.prix} €'})")
        else:
            print(f"Le livre existe déjà : {livre.titre}")

if __name__ == "__main__":
    run()
