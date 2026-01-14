from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser
from formations.models import Programme, Session
from mentoring.models import Mentor
from blog.models import Article, Ressource
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populates the database with initial data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Création des données initiale...')

        # 1. Mentors
        mentor_user, created = CustomUser.objects.get_or_create(
            username='jean_mentor',
            defaults={
                'email': 'jean@atj.com',
                'role': 'mentor'
            }
        )
        if created:
            mentor_user.set_password('mentor123')
            mentor_user.save()
            Mentor.objects.create(
                user=mentor_user,
                bio="Ingénieur informatique avec 10 ans d'expérience.",
                expertise="Développement Web & IA"
            )
            self.stdout.write(' - Mentor Jean créé.')

        alice_user, created = CustomUser.objects.get_or_create(
            username='alice_mentor',
            defaults={
                'email': 'alice@atj.com',
                'role': 'mentor'
            }
        )
        if created:
            alice_user.set_password('mentor123')
            alice_user.save()
            Mentor.objects.create(
                user=alice_user,
                bio="Entrepreneuse et coach en leadership.",
                expertise="Leadership & Management"
            )
            self.stdout.write(' - Mentor Alice créée.')

        # Admin User (just in case)
        admin_user, created = CustomUser.objects.get_or_create(
            username='admin_content',
            defaults={'role': 'admin', 'email': 'content@atj.com'}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.save()


        # 2. Programmes & Sessions
        prog1, _ = Programme.objects.get_or_create(
            titre="Leadership & Confiance",
            defaults={'description': 'Devenez le leader que vous méritez d\'être.'}
        )
        Session.objects.get_or_create(
            programme=prog1,
            date_debut=timezone.now().date() + timedelta(days=10),
            date_fin=timezone.now().date() + timedelta(days=12)
        )

        prog2, _ = Programme.objects.get_or_create(
            titre="Développement Python",
            defaults={'description': 'Apprenez les bases du langage le plus populaire.'}
        )
        Session.objects.get_or_create(
            programme=prog2,
            date_debut=timezone.now().date() + timedelta(days=20),
            date_fin=timezone.now().date() + timedelta(days=25)
        )

        self.stdout.write(' - Programmes et Sessions créés.')

        # 3. Blog Articles
        if not Article.objects.exists():
            Article.objects.create(
                titre="L'importance du mentorat",
                contenu="Le mentorat est un levier puissant pour la réussite...",
                # auteur=admin_user # Removed or needs to be handled if models changed
            )
            Article.objects.create(
                titre="5 Clés pour réussir ses études",
                contenu="L'organisation, la persévérance, ..."
            )
            self.stdout.write(' - Articles de blog créés.')

        # 4. Ressources
        if not Ressource.objects.exists():
            Ressource.objects.create(
                titre="Guide du Leadership (PDF)",
                description="Un guide complet pour débutants.",
                lien_video="https://youtube.com/example"
            )
            self.stdout.write(' - Ressources créées.')

        self.stdout.write(self.style.SUCCESS('Base de données peuplée avec succès !'))
