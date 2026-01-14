import os
import django
from django.utils import timezone
from datetime import timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atj_site.settings')
django.setup()

from accounts.models import CustomUser
from formations.models import Programme, Session
from mentoring.models import Mentor
from blog.models import Article

def run():
    print("Populating database...")

    # Create Programmes
    programs_data = [
        {"titre": "Leadership & Confiance en soi", "desc": "Développez votre charisme et votre impact."},
        {"titre": "Introduction au Python", "desc": "Apprenez les bases de la programmation moderne."},
        {"titre": "Marketing Digital", "desc": "Maîtrisez les réseaux sociaux et la publicité en ligne."},
    ]
    
    for p_data in programs_data:
        prog, created = Programme.objects.get_or_create(
            titre=p_data["titre"],
            defaults={"description": p_data["desc"]}
        )
        if created:
            print(f"Created Programme: {prog.titre}")
            # Create Sessions
            Session.objects.create(
                programme=prog,
                date_debut=timezone.now().date() + timedelta(days=10),
                date_fin=timezone.now().date() + timedelta(days=15)
            )
            Session.objects.create(
                programme=prog,
                date_debut=timezone.now().date() + timedelta(days=30),
                date_fin=timezone.now().date() + timedelta(days=35)
            )
        else:
             print(f"Programme already exists: {prog.titre}")

    # Create Mentors
    mentors_data = [
        {"username": "mentor_alice", "email": "alice@atj.com", "expertise": "Développement Web", "bio": "Experte Django avec 10 ans d'expérience."},
        {"username": "mentor_bob", "email": "bob@atj.com", "expertise": "Marketing & Vente", "bio": "Ancien directeur commercial chez TechCorp."},
    ]

    for m_data in mentors_data:
        user, created = CustomUser.objects.get_or_create(
            username=m_data["username"],
            email=m_data["email"],
            defaults={"role": "mentor"}
        )
        if created:
            user.set_password("password123")
            user.save()
            Mentor.objects.create(
                user=user,
                expertise=m_data["expertise"],
                bio=m_data["bio"]
            )
            print(f"Created Mentor: {m_data['username']}")
        else:
            print(f"Mentor user already exists: {m_data['username']}")

    # Create Articles
    articles_data = [
        {"titre": "L'importance du mentorat", "contenu": "Le mentorat est clé pour réussir... " * 10},
        {"titre": "5 conseils pour votre CV", "contenu": "Un bon CV doit être clair... " * 10},
    ]
    
    for a_data in articles_data:
        art, created = Article.objects.get_or_create(
            titre=a_data["titre"],
            defaults={"contenu": a_data["contenu"]}
        )
        if created:
            print(f"Created Article: {art.titre}")

    print("Database populated successfully!")

if __name__ == '__main__':
    run()
