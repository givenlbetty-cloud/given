"""
Commande de gestion Django pour peupler la base avec des formations génériques.
Usage : python manage.py populate_formations
"""
from django.core.management.base import BaseCommand
from formations.models import Formation, Lecon, Session


class Command(BaseCommand):
    help = "Crée des formations génériques pour illustrer les 5 piliers ATJ."

    def handle(self, *args, **options):
        self._create_art_oratoire()
        self._create_leadership()
        self._create_informatique()
        self._create_langues()
        self._create_affaires()
        self.stdout.write(self.style.SUCCESS("✅ 5 formations créées avec leçons et sessions"))

    # ──────────────────────────────────────────
    # 1. ART ORATOIRE
    # ──────────────────────────────────────────
    def _create_art_oratoire(self):
        f, _ = Formation.objects.get_or_create(
            titre="Art Oratoire – Parler en Public avec Impact",
            defaults={
                "categorie": "art_oratoire",
                "description": (
                    "Maîtrisez l'art de la parole pour convaincre, inspirer et "
                    "captiver votre auditoire. Cette formation vous donne les clés "
                    "pour structurer un discours, gérer le trac et utiliser votre "
                    "voix comme un instrument de persuasion. Que vous soyez étudiant, "
                    "entrepreneur ou professionnel, l'éloquence est un atout "
                    "incontournable dans toutes les sphères de la vie."
                ),
                "prix": 0.00,
                "conditions": "Aucun pré-requis – ouvert à tous.",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Introduction à la prise de parole", "Pourquoi parle-t-on en public ? Les 3 piliers : ethos, pathos, logos."),
            ("Gérer son trac et sa respiration", "Techniques de relaxation et exercices de respiration abdominale."),
            ("Structurer un discours percutant", "Méthode TEDx : accroche, développement, conclusion mémorable."),
            ("Le langage corporel", "Posture, gestuelle, regard : ce que votre corps dit avant vos mots."),
            ("Improviser avec aisance", "Exercices pratiques pour répondre à toute question sans préparation."),
        ])
        Session.objects.get_or_create(
            formation=f,
            type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # ──────────────────────────────────────────
    # 2. LEADERSHIP
    # ──────────────────────────────────────────
    def _create_leadership(self):
        f, _ = Formation.objects.get_or_create(
            titre="Leadership & Confiance en Soi",
            defaults={
                "categorie": "leadership",
                "description": (
                    "Développez votre charisme et votre capacité à mobiliser une "
                    "équipe autour d'une vision commune. Ce parcours alterne théorie "
                    "du leadership moderne et mises en situation concrètes : gestion "
                    "de conflit, motivation d'équipe, intelligence émotionnelle et "
                    "affirmation de soi."
                ),
                "prix": 0.00,
                "conditions": "Ouvert à tous – recommandé pour les porteurs de projet.",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Qu'est-ce qu'un leader ?", "Différence entre chef et leader. Les qualités du leader inspirant."),
            ("Intelligence émotionnelle", "Reconnaître et gérer ses émotions pour mieux interagir."),
            ("Communiquer sa vision", "Créer un message fédérateur et le transmettre avec impact."),
            ("Gestion de conflit", "Médiation, écoute active et recherche de solutions gagnant-gagnant."),
            ("Motiver son équipe au quotidien", "Leviers de motivation intrinsèque et extrinsèque."),
        ])
        Session.objects.get_or_create(
            formation=f,
            type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # ──────────────────────────────────────────
    # 3. INFORMATIQUE
    # ──────────────────────────────────────────
    def _create_informatique(self):
        f, _ = Formation.objects.get_or_create(
            titre="Introduction à l'Informatique & à la Programmation",
            defaults={
                "categorie": "informatique",
                "description": (
                    "Découvrez les fondamentaux de l'informatique : fonctionnement "
                    "d'un ordinateur, logique algorithmique et premiers pas en "
                    "programmation avec Python. Ce cours est conçu pour les grands "
                    "débutants et vous donnera les bases nécessaires pour évoluer "
                    "vers des spécialisations (web, data, IA)."
                ),
                "prix": 0.00,
                "conditions": "Avoir un ordinateur (Windows, Mac ou Linux). Aucune connaissance préalable.",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Qu'est-ce qu'un ordinateur ?", "Hardware, software, système d'exploitation : les bases."),
            ("Introduction aux algorithmes", "Variables, conditions, boucles : la logique avant le code."),
            ("Premiers pas en Python", "Installation, print(), input(), et premières lignes de code."),
            ("Variables et types de données", "Chaînes, entiers, listes : manipuler l'information."),
            ("Fonctions et modules", "Écrire du code réutilisable et importer des bibliothèques."),
        ])
        Session.objects.get_or_create(
            formation=f,
            type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # ──────────────────────────────────────────
    # 4. LANGUES
    # ──────────────────────────────────────────
    def _create_langues(self):
        f, _ = Formation.objects.get_or_create(
            titre="English Fundamentals – Les Bases de l'Anglais",
            defaults={
                "categorie": "langues",
                "description": (
                    "Un cours d'anglais complet pour débutants ou faux-débutants. "
                    "Apprenez le vocabulaire essentiel, les structures grammaticales "
                    "clés et entraînez votre prononciation grâce à des exercices "
                    "interactifs et des mises en situation réelles. À la fin de ce "
                    "parcours, vous serez capable de tenir une conversation simple "
                    "et de comprendre des textes courants."
                ),
                "prix": 0.00,
                "conditions": "Aucun pré-requis – débutants bienvenus.",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Greetings & Introductions", "Hello, how are you? Se présenter, saluer, les formules de politesse."),
            ("Numbers, Dates & Time", "Compter, dire l'heure, les jours de la semaine et les mois."),
            ("Everyday Vocabulary", "Les objets du quotidien, la famille, la nourriture, les couleurs."),
            ("Basic Grammar – Present Simple", "I work, you eat, she speaks. Les verbes réguliers et irréguliers."),
            ("Questions & Answers", "Poser une question ouverte/fermée. Where do you live? What do you do?"),
            ("Listening & Pronunciation", "Compréhension orale avec dialogues simples et exercices de phonétique."),
        ])
        Session.objects.get_or_create(
            formation=f,
            type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # ──────────────────────────────────────────
    # 5. AFFAIRES
    # ──────────────────────────────────────────
    def _create_affaires(self):
        f, _ = Formation.objects.get_or_create(
            titre="Entrepreneuriat & Gestion de Petite Entreprise",
            defaults={
                "categorie": "affaires",
                "description": (
                    "Vous avez une idée de business ? Apprenez à la transformer en "
                    "entreprise viable. Ce cours couvre l'étude de marché, le "
                    "business plan, la comptabilité de base, le marketing digital "
                    "et la gestion de la relation client. Un concentré pratique "
                    "pour lancer et gérer votre activité avec succès."
                ),
                "prix": 0.00,
                "conditions": "Avoir une idée de projet (même vague).",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Trouver et valider son idée", "Étude de marché simplifiée, identifier son client cible."),
            ("Rédiger un Business Plan", "Structure, projections financières et pitch deck."),
            ("Comptabilité et finances de base", "Budget, trésorerie, seuil de rentabilité expliqués simplement."),
            ("Marketing digital pour PME", "Réseaux sociaux, SEO, publicité en ligne avec petit budget."),
            ("Relation client et fidélisation", "Service après-vente, CRM, bouche-à-oreille et avis clients."),
        ])
        Session.objects.get_or_create(
            formation=f,
            type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # ──────────────────────────────────────────
    # Helper
    # ──────────────────────────────────────────
    def _add_lecons(self, formation, lecons_data):
        for i, (titre, contenu) in enumerate(lecons_data, start=1):
            Lecon.objects.get_or_create(
                formation=formation,
                titre=titre,
                defaults={
                    "ordre": i,
                    "contenu_texte": contenu,
                    "duree_minutes": 15,
                    "est_gratuit": True,
                },
            )