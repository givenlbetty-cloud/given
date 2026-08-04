"""
Commande de gestion Django pour peupler la base avec des formations génériques.
Usage : python manage.py populate_formations
"""
from django.core.management.base import BaseCommand
from formations.models import Formation, Lecon, Session


class Command(BaseCommand):
    help = "Crée des formations génériques enrichies pour les 5 piliers ATJ."

    def handle(self, *args, **options):
        self._create_art_oratoire()
        self._create_leadership()
        self._create_informatique()
        self._create_langues()
        self._create_affaires()
        self.stdout.write(self.style.SUCCESS("✅ 5 formations enrichies créées avec leçons détaillées + images"))

    # =====================================================================
    # 1. ART ORATOIRE
    # =====================================================================
    def _create_art_oratoire(self):
        f, _ = Formation.objects.update_or_create(
            titre="Art Oratoire – Parler en Public avec Impact",
            defaults={
                "categorie": "art_oratoire",
                "description": (
                    "La plupart des professions dans la société ne peuvent s'exercer efficacement que si "
                    "l'on a la maîtrise de l'Art de la parole (Avocature, Journalisme, Enseignement, "
                    "Politique, Marketing, Prédication...). Venez apprendre !"
                ),
                "image_couverture": None,
                "prix": 0.00,
                "conditions": "Aucun pré-requis – ouvert à tous.",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Introduction à la prise de parole", """
<h2>Pourquoi apprendre à parler en public ?</h2>
<p>La prise de parole en public est l'une des compétences les plus recherchées dans le monde professionnel. Que vous soyez étudiant, employé ou entrepreneur, savoir vous exprimer clairement devant un groupe est un atout majeur.</p>

<h3>Les 3 piliers de la rhétorique (Aristote)</h3>
<table class="table table-bordered">
<tr><th>Pilier</th><th>Signification</th><th>Exemple</th></tr>
<tr><td><strong>Ethos</strong></td><td>La crédibilité de l'orateur</td><td>Un médecin qui parle de santé</td></tr>
<tr><td><strong>Pathos</strong></td><td>L'émotion suscitée chez l'auditoire</td><td>Raconter une histoire personnelle touchante</td></tr>
<tr><td><strong>Logos</strong></td><td>La logique et les faits</td><td>Présenter des statistiques et des preuves</td></tr>
</table>

<h3>Objectifs de cette formation</h3>
<ul>
<li>Surmonter la peur de parler en public (glossophobie)</li>
<li>Structurer un discours clair et percutant</li>
<li>Utiliser votre voix et votre corps comme des outils de communication</li>
<li>Captiver n'importe quel auditoire, du petit groupe à la grande salle</li>
</ul>
"""),
            ("Gérer son trac et sa respiration", """
<h2>Le trac : un phénomène naturel</h2>
<p>Saviez-vous que <strong>75% des personnes</strong> ressentent de l'anxiété avant de parler en public ? Le trac n'est pas un ennemi : c'est une énergie que vous pouvez canaliser.</p>

<h3>Technique de respiration abdominale (4-4-4-4)</h3>
<ol>
<li><strong>Inspirez</strong> par le nez pendant <strong>4 secondes</strong></li>
<li><strong>Bloquez</strong> votre respiration pendant <strong>4 secondes</strong></li>
<li><strong>Expirez</strong> lentement par la bouche pendant <strong>4 secondes</strong></li>
<li><strong>Attendez</strong> avant de réinspirer pendant <strong>4 secondes</strong></li>
</ol>
<p><em>Répétez ce cycle 5 fois avant de prendre la parole.</em></p>

<h3>Exercice pratique : La visualisation positive</h3>
<p>Fermez les yeux 2 minutes avant votre intervention. Imaginez-vous en train de réussir : le public sourit, applaudit, vous vous sentez confiant. Votre cerveau ne fait pas la différence entre une expérience vécue et une expérience visualisée intensément.</p>
"""),
            ("Structurer un discours percutant", """
<h2>La méthode TEDx en 3 actes</h2>
<p>Les conférences TED sont célèbres pour leur format percutant. Voici leur structure secrète :</p>

<h3>Acte 1 : L'accroche (30 secondes)</h3>
<ul>
<li>Commencez par une <strong>question choc</strong> ou une <strong>statistique surprenante</strong></li>
<li>Exemple : "Saviez-vous que 90% des gens oublient votre message dans les 24h ?"</li>
<li>Ou racontez une <strong>anecdote personnelle</strong> en 2 phrases</li>
</ul>

<h3>Acte 2 : Le développement (3-5 minutes)</h3>
<ul>
<li>Présentez <strong>3 idées principales</strong> maximum (la règle de 3)</li>
<li>Illustrez chaque idée avec un exemple concret</li>
<li>Utilisez des transitions claires : "Premièrement... Deuxièmement... Enfin..."</li>
</ul>

<h3>Acte 3 : La conclusion mémorable (30 secondes)</h3>
<ul>
<li>Résumez en UNE phrase votre message clé</li>
<li>Terminez par un <strong>appel à l'action</strong> : "Alors, qu'allez-vous faire différemment dès demain ?"</li>
</ul>
"""),
            ("Le langage corporel", """
<h2>Votre corps parle avant vous</h2>
<p>Des études montrent que <strong>55% de l'impact d'un message</strong> vient du langage corporel, contre seulement 7% pour les mots eux-mêmes.</p>

<h3>Les 5 règles d'or de la posture</h3>
<ol>
<li><strong>Ancrez vos pieds</strong> : écartés à la largeur des épaules, poids réparti également</li>
<li><strong>Ouvrez votre poitrine</strong> : épaules en arrière, dos droit (posture de confiance)</li>
<li><strong>Libérez vos mains</strong> : utilisez des gestes ouverts, paumes visibles</li>
<li><strong>Regardez dans les yeux</strong> : balayez la salle en "W" (gauche, droite, centre)</li>
<li><strong>Souriez</strong> : un sourire authentique détend l'auditoire et l'orateur</li>
</ol>

<h3>À ÉVITER absolument</h3>
<ul>
<li>❌ Les mains dans les poches</li>
<li>❌ Se balancer d'un pied sur l'autre</li>
<li>❌ Fixer le sol ou le plafond</li>
<li>❌ Croiser les bras (signe de fermeture)</li>
</ul>
"""),
            ("Improviser avec aisance", """
<h2>L'improvisation ne s'improvise pas !</h2>
<p>Les meilleurs orateurs ne sont pas ceux qui ont un texte parfait : ce sont ceux qui savent <strong>rebondir</strong> quand l'inattendu survient.</p>

<h3>La méthode PREP (Point-Reason-Example-Point)</h3>
<p>Quand on vous pose une question inattendue, structurez votre réponse en 4 étapes :</p>
<ol>
<li><strong>Point</strong> : Énoncez votre idée principale en une phrase</li>
<li><strong>Reason</strong> : Donnez la raison qui justifie votre point de vue</li>
<li><strong>Example</strong> : Illustrez avec un exemple concret ou une anecdote</li>
<li><strong>Point</strong> : Reformulez votre idée pour conclure</li>
</ol>

<h3>Exercice : Le "Oui, et..."</h3>
<p>En improvisation théâtrale, la règle d'or est de ne jamais dire "non" mais d'accepter et d'ajouter. Entraînez-vous avec un ami : l'un lance une idée absurde, l'autre répond "Oui, et..." et développe.</p>
<p><em>Exemple : "Je crois que les chats devraient diriger le monde." → "Oui, et ils instaureraient des siestes obligatoires de 14h à 16h !"</em></p>
"""),
        ])
        Session.objects.get_or_create(
            formation=f, type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # =====================================================================
    # 2. LEADERSHIP
    # =====================================================================
    def _create_leadership(self):
        f, _ = Formation.objects.update_or_create(
            titre="Leadership & Confiance en Soi",
            defaults={
                "categorie": "leadership",
                "description": (
                    "Coaching pratique sur mesure, développement d'un leadership responsable, motivationnel "
                    "et fondé sur l'intelligence émotionnelle."
                ),
                "image_couverture": None,
                "prix": 0.00,
                "conditions": "Ouvert à tous – recommandé pour les porteurs de projet.",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Qu'est-ce qu'un leader ?", """
<h2>Leader ≠ Chef</h2>
<p>Un <strong>chef</strong> donne des ordres. Un <strong>leader</strong> donne une direction. Le chef se fait obéir par la hiérarchie; le leader se fait suivre par l'inspiration.</p>

<h3>Les 5 qualités du leader inspirant</h3>
<table class="table table-bordered">
<tr><th>Qualité</th><th>Description</th></tr>
<tr><td>1. Vision</td><td>Voir l'avenir et le communiquer avec clarté</td></tr>
<tr><td>2. Intégrité</td><td>Agir selon des valeurs cohérentes, montrer l'exemple</td></tr>
<tr><td>3. Empathie</td><td>Comprendre les émotions et besoins de son équipe</td></tr>
<tr><td>4. Courage</td><td>Prendre des décisions difficiles face à l'incertitude</td></tr>
<tr><td>5. Humilité</td><td>Reconnaître ses erreurs et valoriser les autres</td></tr>
</table>

<h3>Exercice : Identifiez votre style de leadership</h3>
<p>Il existe 4 styles principaux : <strong>Directif, Participatif, Délégatif, Coach</strong>. Aucun n'est meilleur que l'autre — tout dépend du contexte. Dans quelle situation chaque style est-il le plus adapté ?</p>
"""),
            ("Intelligence émotionnelle", """
<h2>Le quotient émotionnel (QE) : plus important que le QI ?</h2>
<p>Daniel Goleman a démontré que <strong>90% des leaders les plus performants</strong> ont un QE élevé. L'intelligence émotionnelle, c'est la capacité à reconnaître, comprendre et gérer ses émotions ET celles des autres.</p>

<h3>Les 4 piliers de l'intelligence émotionnelle</h3>
<ol>
<li><strong>Conscience de soi</strong> : Reconnaître ses émotions au moment où elles surviennent</li>
<li><strong>Maîtrise de soi</strong> : Garder le contrôle face au stress, à la colère ou la frustration</li>
<li><strong>Empathie</strong> : Ressentir ce que l'autre ressent, se mettre à sa place</li>
<li><strong>Compétences sociales</strong> : Influencer, motiver, résoudre les conflits</li>
</ol>

<h3>Exercice : Le journal émotionnel</h3>
<p>Pendant une semaine, notez chaque soir : (1) quelle émotion forte avez-vous ressentie aujourd'hui ? (2) qu'est-ce qui l'a déclenchée ? (3) comment avez-vous réagi ? (4) que feriez-vous différemment ?</p>
"""),
            ("Communiquer sa vision", """
<h2>Une vision sans communication n'est qu'un rêve</h2>
<p>Martin Luther King n'a pas dit "J'ai un plan stratégique". Il a dit <strong>"I have a dream"</strong>. La différence ? La vision se ressent, le plan se comprend.</p>

<h3>Les 4 éléments d'une vision qui fédère</h3>
<ol>
<li><strong>Clarté</strong> : Une phrase que tout le monde peut répéter</li>
<li><strong>Émotion</strong> : Une image qui donne envie de se lever le matin</li>
<li><strong>Ambition</strong> : Un objectif qui fait un peu peur (sinon c'est trop facile)</li>
<li><strong>Connexion</strong> : Un lien direct avec le quotidien de chacun</li>
</ol>

<h3>Exemple de vision mal formulée vs bien formulée</h3>
<p>❌ "Nous voulons être le leader du marché des solutions digitales B2B d'ici 2030."</p>
<p>✅ "Nous allons permettre à chaque petite entreprise africaine d'avoir une vitrine en ligne aussi belle que celle des géants du e-commerce."</p>
"""),
            ("Gestion de conflit", """
<h2>Le conflit n'est pas le problème : l'évitement l'est</h2>
<p>Un conflit bien géré renforce une équipe. Un conflit ignoré la détruit de l'intérieur. Voici comment transformer un désaccord en opportunité de croissance.</p>

<h3>La méthode DESC (communication non-violente)</h3>
<ol>
<li><strong>Décrire</strong> : Exposez les faits, sans jugement. "Quand tu arrives 15 minutes en retard aux réunions..."</li>
<li><strong>Exprimer</strong> : Partagez votre ressenti. "Je me sens frustré car nous perdons du temps..."</li>
<li><strong>Spécifier</strong> : Proposez une solution concrète. "Pourrions-nous convenir de commencer à l'heure exacte ?"</li>
<li><strong>Conclure</strong> : Énoncez le bénéfice mutuel. "Ainsi nous finirons plus tôt et tout le monde sera satisfait."</li>
</ol>

<h3>Les 5 erreurs à éviter en cas de conflit</h3>
<ul>
<li>❌ Attaquer la personne au lieu du comportement</li>
<li>❌ Accumuler des reproches anciens ("et en plus, le mois dernier...")</li>
<li>❌ Utiliser des généralisations ("tu es TOUJOURS en retard")</li>
<li>❌ Refuser d'écouter la version de l'autre</li>
<li>❌ Laisser le conflit pourrir en espérant qu'il disparaisse</li>
</ul>
"""),
            ("Motiver son équipe au quotidien", """
<h2>La motivation ne se décrète pas, elle se cultive</h2>
<p>Un salaire élevé ne suffit pas à motiver durablement. Selon la <strong>théorie de l'autodétermination</strong>, trois besoins psychologiques fondamentaux doivent être satisfaits :</p>

<h3>Les 3 leviers de motivation</h3>
<table class="table table-bordered">
<tr><th>Besoin</th><th>Comment le satisfaire</th></tr>
<tr><td><strong>Autonomie</strong></td><td>Laissez vos collaborateurs choisir COMMENT atteindre l'objectif. Ne micro-managez pas.</td></tr>
<tr><td><strong>Compétence</strong></td><td>Proposez des formations, donnez du feedback positif, célébrez les progrès.</td></tr>
<tr><td><strong>Appartenance</strong></td><td>Créez des rituels d'équipe, valorisez la contribution de chacun au projet commun.</td></tr>
</table>

<h3>Action simple pour demain matin</h3>
<p>Envoyez un message à UN membre de votre équipe pour lui dire précisément ce que vous avez apprécié dans son travail cette semaine. Pas un "bon boulot" vague — un compliment SPÉCIFIQUE. L'impact sera immédiat.</p>
"""),
        ])
        Session.objects.get_or_create(
            formation=f, type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # =====================================================================
    # 3. INFORMATIQUE
    # =====================================================================
    def _create_informatique(self):
        f, _ = Formation.objects.update_or_create(
            titre="Introduction à l'Informatique & à la Programmation",
            defaults={
                "categorie": "informatique",
                "description": (
                    "Maîtrise des logiciels de bureautique (Word, Publisher, PowerPoint, Excel, etc.), "
                    "design graphique et techniques d'imprimerie."
                ),
                "image_couverture": None,
                "prix": 0.00,
                "conditions": "Avoir un ordinateur (Windows, Mac ou Linux). Aucune connaissance préalable.",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Qu'est-ce qu'un ordinateur ?", """
<h2>L'ordinateur : un outil, pas une boîte magique</h2>
<p>Un ordinateur est une machine qui exécute des instructions. Rien de plus. La puissance vient de sa capacité à exécuter des <strong>milliards d'instructions par seconde</strong>.</p>

<h3>Les 4 composants fondamentaux</h3>
<table class="table table-bordered">
<tr><th>Composant</th><th>Rôle</th><th>Analogie humaine</th></tr>
<tr><td><strong>Processeur (CPU)</strong></td><td>Exécute les calculs et les instructions</td><td>Le cerveau</td></tr>
<tr><td><strong>Mémoire vive (RAM)</strong></td><td>Stockage temporaire, rapide, effacé à l'extinction</td><td>La mémoire à court terme</td></tr>
<tr><td><strong>Disque dur (HDD/SSD)</strong></td><td>Stockage permanent des fichiers et logiciels</td><td>La mémoire à long terme</td></tr>
<tr><td><strong>Carte mère</strong></td><td>Relie tous les composants entre eux</td><td>Le système nerveux</td></tr>
</table>

<h3>Logiciel vs Matériel</h3>
<p>Le <strong>hardware</strong> (matériel) est tout ce que vous pouvez toucher. Le <strong>software</strong> (logiciel) est l'ensemble des programmes qui donnent des instructions au matériel. Le système d'exploitation (Windows, macOS, Linux) est le chef d'orchestre entre les deux.</p>
"""),
            ("Introduction aux algorithmes", """
<h2>Un algorithme, c'est une recette de cuisine</h2>
<p>Imaginez une recette de gâteau : vous avez une liste d'ingrédients (les entrées), une série d'étapes à suivre dans l'ordre (les instructions), et le gâteau à la fin (la sortie). Un algorithme, c'est exactement cela.</p>

<h3>Les 3 structures fondamentales</h3>
<ol>
<li><strong>La séquence</strong> : les instructions s'exécutent l'une après l'autre, dans l'ordre.</li>
<li><strong>La condition (SI...ALORS)</strong> : "SI l'œuf est cassé, ALORS le jeter, SINON le casser dans le bol."</li>
<li><strong>La boucle (RÉPÉTER)</strong> : "Battre les œufs JUSQU'À ce que le mélange soit mousseux."</li>
</ol>

<h3>Exercice : Écrivez un algorithme</h3>
<p>Décrivez, étape par étape, comment préparer un café. Chaque étape doit être suffisamment précise pour qu'un robot (qui ne sait RIEN) puisse l'exécuter. C'est exactement ce qu'est un programme informatique.</p>
"""),
            ("Premiers pas en Python", """
<h2>Pourquoi Python ?</h2>
<p>Python est le langage de programmation le plus utilisé au monde pour l'apprentissage, la data science et l'intelligence artificielle. Sa syntaxe est proche de l'anglais, ce qui le rend <strong>très lisible</strong>.</p>

<h3>Votre premier programme</h3>
<pre><code># Ceci est un commentaire (ignoré par l'ordinateur)
print("Hello, World!")  # Affiche un message à l'écran

# Demander le nom de l'utilisateur
nom = input("Quel est ton nom ? ")
print("Enchanté, " + nom + " !")
</code></pre>

<h3>Comment exécuter ce code</h3>
<ol>
<li>Téléchargez Python sur <strong>python.org</strong> (gratuit)</li>
<li>Ouvrez l'application <strong>IDLE</strong> (installée avec Python)</li>
<li>Tapez les lignes de code ci-dessus</li>
<li>Appuyez sur F5 pour exécuter</li>
</ol>

<p><em>Félicitations ! Vous venez d'écrire votre premier programme interactif.</em></p>
"""),
            ("Variables et types de données", """
<h2>Une variable, c'est une boîte étiquetée</h2>
<p>Imaginez une boîte sur laquelle vous collez une étiquette "âge". À l'intérieur, vous mettez le nombre 25. En programmation, c'est exactement cela :</p>
<pre><code>age = 25          # un nombre entier (int)
prenom = "Marie"    # une chaîne de caractères (str)
taille = 1.68       # un nombre décimal (float)
est_etudiant = True # un booléen (True/False)
</code></pre>

<h3>Les 4 types de données principaux</h3>
<table class="table table-bordered">
<tr><th>Type</th><th>Nom Python</th><th>Exemple</th></tr>
<tr><td>Nombre entier</td><td><code>int</code></td><td>42, -7, 0</td></tr>
<tr><td>Nombre décimal</td><td><code>float</code></td><td>3.14, -0.5</td></tr>
<tr><td>Texte</td><td><code>str</code></td><td>"Bonjour", 'a'</td></tr>
<tr><td>Vrai/Faux</td><td><code>bool</code></td><td>True, False</td></tr>
</table>

<h3>Opérations de base</h3>
<pre><code>a = 10
b = 3
print(a + b)   # 13 (addition)
print(a - b)   # 7  (soustraction)
print(a * b)   # 30 (multiplication)
print(a / b)   # 3.333... (division)
print(a % b)   # 1  (reste de la division)
</code></pre>
"""),
            ("Fonctions et modules", """
<h2>Une fonction : un bloc d'instructions réutilisable</h2>
<p>Imaginez que vous deviez calculer la TVA sur des centaines de produits. Plutôt que de répéter le même calcul, vous créez une <strong>fonction</strong> — un petit programme que vous pouvez appeler à volonté.</p>

<h3>Exemple de fonction</h3>
<pre><code>def calculer_tva(prix_ht):
    "Calcule le prix TTC à partir du prix HT"
    tva = prix_ht * 0.16  # TVA à 16% (RDC)
    prix_ttc = prix_ht + tva
    return prix_ttc

# Utilisation
print(calculer_tva(100))  # 116.0
print(calculer_tva(250))  # 290.0
print(calculer_tva(500))  # 580.0
</code></pre>

<h3>Les modules : des bibliothèques de fonctions prêtes à l'emploi</h3>
<p>Python est livré avec des centaines de modules. Au lieu de tout réinventer, vous importez ce dont vous avez besoin :</p>
<pre><code>import math
print(math.sqrt(16))  # 4.0 (racine carrée)

import random
print(random.randint(1, 6))  # Simule un lancer de dé
</code></pre>
"""),
        ])
        Session.objects.get_or_create(
            formation=f, type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # =====================================================================
    # 4. LANGUES (Anglais)
    # =====================================================================
    def _create_langues(self):
        f, _ = Formation.objects.update_or_create(
            titre="English Fundamentals – Les Bases de l'Anglais",
            defaults={
                "categorie": "langues",
                "description": (
                    "Un cours d'anglais complet pour débutants ou faux-débutants. Apprenez le vocabulaire "
                    "essentiel, les structures grammaticales clés et entraînez votre prononciation grâce à "
                    "des exercices interactifs et des mises en situation réelles. À la fin de ce parcours, "
                    "vous serez capable de tenir une conversation simple et de comprendre des textes courants."
                ),
                "image_couverture": None,
                "prix": 0.00,
                "conditions": "Aucun pré-requis – débutants bienvenus.",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Lesson 1 – Greetings & Introductions", """
<h2>Welcome to English! 🇬🇧</h2>
<p>Dans cette première leçon, vous allez apprendre à saluer, vous présenter et répondre aux questions de base. C'est la compétence la plus importante pour commencer toute conversation.</p>

<h3>Les salutations (Greetings)</h3>
<table class="table table-bordered">
<tr><th>Anglais</th><th>Français</th><th>Quand l'utiliser ?</th></tr>
<tr><td>Hello / Hi</td><td>Bonjour / Salut</td><td>À tout moment, formel ou informel</td></tr>
<tr><td>Good morning</td><td>Bonjour (matin)</td><td>Avant midi</td></tr>
<tr><td>Good afternoon</td><td>Bon(ne) après-midi</td><td>Entre midi et 18h</td></tr>
<tr><td>Good evening</td><td>Bonsoir</td><td>Après 18h</td></tr>
<tr><td>Goodbye / Bye</td><td>Au revoir</td><td>Pour prendre congé</td></tr>
</table>

<h3>Se présenter (Introduce yourself)</h3>
<pre><code>Hello! My name is John. I am from Canada.
Nice to meet you!

Bonjour ! Je m'appelle John. Je viens du Canada.
Enchanté(e) de vous rencontrer !</code></pre>

<h3>Dialogue modèle</h3>
<div style="background:#f8f9fa;padding:15px;border-radius:8px;">
<p><strong>A:</strong> Hello! How are you?<br>
<strong>B:</strong> I'm fine, thank you. And you?<br>
<strong>A:</strong> I'm good, thanks. My name is Sarah. What's your name?<br>
<strong>B:</strong> Nice to meet you, Sarah. I'm David.<br>
<strong>A:</strong> Nice to meet you too, David!</p>
</div>

<h3>À retenir</h3>
<ul>
<li>"How are you?" = "Comment allez-vous ?" — la réponse classique est "I'm fine, thank you"</li>
<li>"What's your name?" = "Quel est votre nom ?"</li>
<li>"Nice to meet you" = "Enchanté(e)"</li>
</ul>
"""),
            ("Lesson 2 – Numbers, Dates & Time", """
<h2>Les nombres en anglais</h2>
<p>Maîtriser les nombres est essentiel pour donner son âge, un numéro de téléphone ou comprendre les prix.</p>

<h3>Compter de 1 à 20</h3>
<table class="table table-bordered table-sm">
<tr><td>1 – one</td><td>6 – six</td><td>11 – eleven</td><td>16 – sixteen</td></tr>
<tr><td>2 – two</td><td>7 – seven</td><td>12 – twelve</td><td>17 – seventeen</td></tr>
<tr><td>3 – three</td><td>8 – eight</td><td>13 – thirteen</td><td>18 – eighteen</td></tr>
<tr><td>4 – four</td><td>9 – nine</td><td>14 – fourteen</td><td>19 – nineteen</td></tr>
<tr><td>5 – five</td><td>10 – ten</td><td>15 – fifteen</td><td>20 – twenty</td></tr>
</table>

<h3>Les jours de la semaine (Days of the week)</h3>
<p><strong>Monday</strong> (lundi) · <strong>Tuesday</strong> (mardi) · <strong>Wednesday</strong> (mercredi)<br>
<strong>Thursday</strong> (jeudi) · <strong>Friday</strong> (vendredi) · <strong>Saturday</strong> (samedi) · <strong>Sunday</strong> (dimanche)</p>

<h3>Dire l'heure (Telling the time)</h3>
<table class="table table-bordered">
<tr><th>Heure</th><th>Anglais</th></tr>
<tr><td>8:00</td><td>It's eight o'clock</td></tr>
<tr><td>8:15</td><td>It's quarter past eight</td></tr>
<tr><td>8:30</td><td>It's half past eight</td></tr>
<tr><td>8:45</td><td>It's quarter to nine</td></tr>
</table>
<p><em>💡 Astuce : Au-delà de la demi-heure, on compte les minutes jusqu'à l'heure suivante. "8:50" = "It's ten to nine" (il est dix minutes avant neuf heures).</em></p>
"""),
            ("Lesson 3 – Everyday Vocabulary", """
<h2>Le vocabulaire du quotidien</h2>
<p>Apprendre des listes de mots est plus efficace quand on les regroupe par thème. Voici les 50 mots les plus utiles au quotidien.</p>

<h3>La famille (Family)</h3>
<table class="table table-bordered table-sm">
<tr><td>Mother / Mom</td><td>Mère / Maman</td><td>Father / Dad</td><td>Père / Papa</td></tr>
<tr><td>Sister</td><td>Sœur</td><td>Brother</td><td>Frère</td></tr>
<tr><td>Daughter</td><td>Fille</td><td>Son</td><td>Fils</td></tr>
<tr><td>Grandmother</td><td>Grand-mère</td><td>Grandfather</td><td>Grand-père</td></tr>
</table>

<h3>La nourriture (Food)</h3>
<table class="table table-bordered table-sm">
<tr><td>Bread</td><td>Pain</td><td>Rice</td><td>Riz</td><td>Chicken</td><td>Poulet</td></tr>
<tr><td>Water</td><td>Eau</td><td>Milk</td><td>Lait</td><td>Egg</td><td>Œuf</td></tr>
<tr><td>Fruit</td><td>Fruit</td><td>Vegetable</td><td>Légume</td><td>Fish</td><td>Poisson</td></tr>
</table>

<h3>Les couleurs (Colors)</h3>
<p>🔴 Red · 🔵 Blue · 🟢 Green · 🟡 Yellow · ⚫ Black · ⚪ White · 🟠 Orange · 🟣 Purple · 🟤 Brown · 🩶 Gray</p>

<h3>Exercice : Étiquetez votre environnement</h3>
<p>Prenez des post-its et collez le mot anglais sur TOUS les objets de votre maison : "door" sur la porte, "mirror" sur le miroir, "fridge" sur le frigo. Changez-les chaque semaine avec de nouveaux mots.</p>
"""),
            ("Lesson 4 – Basic Grammar: Present Simple", """
<h2>Le Présent Simple : la base de la grammaire anglaise</h2>
<p>Le Present Simple s'utilise pour parler d'habitudes, de faits généraux et de vérités permanentes.</p>

<h3>Règle d'or</h3>
<div style="background:#e8f5e9;padding:15px;border-radius:8px;border-left:4px solid #4caf50;">
<p><strong>Sujet + Verbe</strong></p>
<p>MAIS avec <strong>he / she / it</strong>, on ajoute <strong>-s</strong> (ou -es) au verbe !</p>
</div>

<h3>Exemples</h3>
<table class="table table-bordered">
<tr><th>Sujet</th><th>Verbe (to work = travailler)</th><th>Traduction</th></tr>
<tr><td>I</td><td>work</td><td>Je travaille</td></tr>
<tr><td>You</td><td>work</td><td>Tu travailles</td></tr>
<tr><td>He / She / It</td><td>work<strong>s</strong></td><td>Il/Elle travaille</td></tr>
<tr><td>We</td><td>work</td><td>Nous travaillons</td></tr>
<tr><td>They</td><td>work</td><td>Ils/Elles travaillent</td></tr>
</table>

<h3>La négation et la question</h3>
<pre><code>I don't work.        (Je ne travaille PAS.)
He doesn't work.     (Il ne travaille PAS.)
Do you work?         (Travailles-tu ?)
Does she work?       (Travaille-t-elle ?)</code></pre>

<h3>Exercice : Complétez</h3>
<p>1. She _____ (to eat) rice every day.<br>
2. They _____ (to live) in Lubumbashi.<br>
3. _____ he _____ (to like) football?</p>
<p><em>Réponses : 1. eats | 2. live | 3. Does...like</em></p>
"""),
            ("Lesson 5 – Questions & Answers", """
<h2>Poser une question, c'est ouvrir une porte</h2>
<p>En anglais, la plupart des questions suivent une structure simple. Maîtrisez-la et vous pourrez demander presque tout ce que vous voulez.</p>

<h3>Les mots interrogatifs (WH- words)</h3>
<table class="table table-bordered">
<tr><th>Mot</th><th>Utilisation</th><th>Exemple</th></tr>
<tr><td>What</td><td>Quoi / Que</td><td>What is your name?</td></tr>
<tr><td>Where</td><td>Où</td><td>Where do you live?</td></tr>
<tr><td>When</td><td>Quand</td><td>When is your birthday?</td></tr>
<tr><td>Who</td><td>Qui</td><td>Who is your teacher?</td></tr>
<tr><td>Why</td><td>Pourquoi</td><td>Why are you learning English?</td></tr>
<tr><td>How</td><td>Comment</td><td>How are you? / How do you go to work?</td></tr>
</table>

<h3>Structure d'une question</h3>
<pre><code>Wh- + Auxiliaire + Sujet + Verbe + ?

Where   do         you     live  ?
What    does       she     like  ?
How     is         he      today ?</code></pre>

<h3>Dialogue : Poser des questions</h3>
<div style="background:#f8f9fa;padding:15px;border-radius:8px;">
<p><strong>A:</strong> What do you do? (Que faites-vous dans la vie ?)<br>
<strong>B:</strong> I'm a student. And you?<br>
<strong>A:</strong> I work in a hospital. Where are you from?<br>
<strong>B:</strong> I'm from Kinshasa. How about you?<br>
<strong>A:</strong> I'm from Lubumbashi.</p>
</div>
"""),
            ("Lesson 6 – Listening & Pronunciation", """
<h2>Comprendre l'anglais parlé</h2>
<p>La compréhension orale est souvent la compétence la plus difficile. Voici comment progresser efficacement, même sans vivre dans un pays anglophone.</p>

<h3>Les 3 techniques pour améliorer votre oreille</h3>
<ol>
<li><strong>Écouter sans comprendre (bain linguistique)</strong> : Mettez une radio anglaise (BBC, NPR) en fond sonore pendant 30 minutes par jour. Votre cerveau s'habitue aux sons, même si vous ne comprenez pas tout.</li>
<li><strong>Écouter ET lire (shadowing)</strong> : Trouvez une vidéo YouTube avec sous-titres. Écoutez une phrase, mettez pause, répétez à voix haute en imitant l'accent. C'est l'exercice le plus efficace.</li>
<li><strong>Dictée active</strong> : Écoutez un court extrait (30 secondes). Essayez d'écrire ce que vous entendez. Recommencez 3 fois. Puis vérifiez avec les sous-titres.</li>
</ol>

<h3>Les sons difficiles pour les francophones</h3>
<table class="table table-bordered">
<tr><th>Son</th><th>Problème</th><th>Exemple</th></tr>
<tr><td><strong>TH</strong> (comme dans "the")</td><td>La langue touche les dents du haut</td><td>the, this, that, think, three</td></tr>
<tr><td><strong>H</strong> aspiré</td><td>On doit entendre le souffle</td><td>hello, happy, help, house</td></tr>
<tr><td><strong>R</strong> anglais</td><td>La langue ne touche pas le palais</td><td>red, right, run, car, water</td></tr>
</table>

<h3>Ressources gratuites recommandées</h3>
<ul>
<li>📺 <strong>BBC Learning English</strong> sur YouTube – leçons courtes et claires</li>
<li>📱 <strong>Duolingo</strong> (application mobile) – 5 minutes par jour</li>
<li>🎧 <strong>Podcast "6 Minute English"</strong> (BBC) – dialogues simples en 6 minutes</li>
</ul>
"""),
        ])
        Session.objects.get_or_create(
            formation=f, type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # =====================================================================
    # 5. AFFAIRES
    # =====================================================================
    def _create_affaires(self):
        f, _ = Formation.objects.update_or_create(
            titre="Entrepreneuriat & Gestion de Petite Entreprise",
            defaults={
                "categorie": "affaires",
                "description": (
                    "Vous avez une idée de business ? Apprenez à la transformer en entreprise viable. "
                    "Ce cours couvre l'étude de marché, le business plan, la comptabilité de base, le "
                    "marketing digital et la gestion de la relation client. Un concentré pratique pour "
                    "lancer et gérer votre activité avec succès."
                ),
                "image_couverture": None,
                "prix": 0.00,
                "conditions": "Avoir une idée de projet (même vague).",
                "est_publie": True,
            },
        )
        self._add_lecons(f, [
            ("Trouver et valider son idée", """
<h2>La meilleure idée du monde ne vaut rien sans clients</h2>
<p>90% des startups échouent. La raison n°1 ? <strong>Elles créent un produit dont personne ne veut.</strong> Voici comment éviter ce piège.</p>

<h3>Les 4 questions à se poser AVANT de se lancer</h3>
<ol>
<li><strong>Quel problème</strong> est-ce que je résous ? (pas "quel produit je vends")</li>
<li><strong>Qui</strong> a ce problème ? (âge, localisation, revenus, habitudes)</li>
<li><strong>Comment</strong> ces personnes résolvent-elles ce problème aujourd'hui ?</li>
<li><strong>Pourquoi</strong> ma solution est-elle meilleure / moins chère / plus rapide ?</li>
</ol>

<h3>Étude de marché simplifiée (en 1 journée)</h3>
<ol>
<li>Allez sur les réseaux sociaux et lisez les commentaires de vos concurrents. Qu'est-ce que les clients se plaignent ? C'est votre opportunité.</li>
<li>Posez la question à 10 personnes de votre cible : "Quel est votre plus gros problème avec [votre domaine] ?" Écoutez sans interrompre.</li>
<li>Analysez les mots-clés recherchés sur Google avec <strong>Google Trends</strong> (gratuit).</li>
</ol>
"""),
            ("Rédiger un Business Plan", """
<h2>Un business plan n'est pas un roman — c'est une feuille de route</h2>
<p>Les investisseurs passent en moyenne <strong>3 minutes</strong> sur un business plan. Il doit donc être clair, concis et percutant.</p>

<h3>Structure en 7 sections</h3>
<ol>
<li><strong>Résumé exécutif (1 page)</strong> : Le problème, votre solution, le marché, vos chiffres clés. C'est la seule page que beaucoup liront.</li>
<li><strong>Description du projet</strong> : Qui êtes-vous ? Que vendez-vous ? Pourquoi maintenant ?</li>
<li><strong>Étude de marché</strong> : Taille du marché, clients cibles, concurrents, votre avantage</li>
<li><strong>Stratégie marketing</strong> : Comment allez-vous trouver vos clients ? Quel budget ?</li>
<li><strong>Plan opérationnel</strong> : Qui fait quoi ? Quels sont vos fournisseurs ?</li>
<li><strong>Plan financier</strong> : Combien ça coûte ? Combien ça rapporte ? Quand serez-vous rentable ?</li>
<li><strong>Annexes</strong> : CV, études, devis, lettres d'intention</li>
</ol>

<h3>Outil gratuit recommandé</h3>
<p>Utilisez <strong>Canva</strong> ou <strong>Google Docs</strong> pour créer un business plan visuel. Évitez les pavés de texte : un graphique vaut 1000 mots.</p>
"""),
            ("Comptabilité et finances de base", """
<h2>La comptabilité n'est pas compliquée — elle est essentielle</h2>
<p>Beaucoup de petits entrepreneurs négligent la comptabilité... jusqu'au jour où ils n'ont plus de trésorerie. Voici les 3 concepts que vous devez absolument maîtriser.</p>

<h3>1. Le compte de résultat (ai-je gagné ou perdu ?)</h3>
<pre><code>CHIFFRE D'AFFAIRES (ventes)
- CHARGES (loyer, salaires, matières premières...)
= RÉSULTAT (bénéfice ou perte)</code></pre>

<h3>2. Le seuil de rentabilité</h3>
<p>C'est le <strong>montant minimum de ventes</strong> que vous devez réaliser pour ne pas perdre d'argent. Formule simple :</p>
<pre><code>Seuil = Charges fixes ÷ Marge par produit</code></pre>
<p><em>Exemple : Si vos charges fixes sont de 500€/mois et que vous gagnez 10€ par produit vendu, vous devez vendre 50 produits par mois pour être à l'équilibre.</em></p>

<h3>3. La trésorerie (le nerf de la guerre)</h3>
<p>La trésorerie, c'est l'argent DISPONIBLE sur votre compte bancaire. On peut être rentable... et en faillite si les clients paient trop tard. Surveillez votre trésorerie chaque semaine, pas chaque mois.</p>
"""),
            ("Marketing digital pour PME", """
<h2>Pas besoin d'un gros budget pour être visible</h2>
<p>Avec les bons outils gratuits et une stratégie cohérente, une petite entreprise peut rivaliser avec les grands groupes en ligne.</p>

<h3>Les 4 canaux essentiels (et gratuits)</h3>
<table class="table table-bordered">
<tr><th>Canal</th><th>Pourquoi ?</th><th>Action immédiate</th></tr>
<tr><td><strong>Google My Business</strong></td><td>Apparaître sur Google Maps gratuitement</td><td>Créez votre fiche et demandez 5 avis clients cette semaine</td></tr>
<tr><td><strong>Facebook / Instagram</strong></td><td>Toucher votre communauté locale</td><td>Publiez 3x/semaine : un conseil, une photo de produit, un témoignage</td></tr>
<tr><td><strong>WhatsApp Business</strong></td><td>Relation client directe et gratuite</td><td>Créez un catalogue de produits et une réponse automatique</td></tr>
<tr><td><strong>SEO (Google)</strong></td><td>Être trouvé par ceux qui cherchent</td><td>Identifiez 5 mots-clés et écrivez un article par semaine</td></tr>
</table>

<h3>La règle des 80/20 du contenu</h3>
<p>80% de contenu UTILE (conseils, tutoriels, histoires) — 20% de contenu PROMOTIONNEL. Si vous ne faites que de la pub, les gens s'en vont. Si vous aidez, ils restent et achètent.</p>
"""),
            ("Relation client et fidélisation", """
<h2>Garder un client coûte 5x moins cher qu'en acquérir un nouveau</h2>
<p>La fidélisation est le levier de croissance le plus négligé par les petites entreprises.</p>

<h3>Les 3 piliers de la fidélisation</h3>
<ol>
<li><strong>Service après-vente irréprochable</strong> : Répondez en moins d'1 heure. Résolvez le problème avant que le client ne le demande. Remplacez le produit sans discuter.</li>
<li><strong>Programme de fidélité simple</strong> : "10 achats = 1 produit offert". Pas besoin de carte compliquée — un tampon sur un papier suffit.</li>
<li><strong>Communication régulière</strong> : Un message WhatsApp par mois pour prendre des nouvelles. Pas de publicité — juste "Comment allez-vous ? Votre dernier achat vous satisfait-il ?"</li>
</ol>

<h3>La méthode AURA pour traiter une réclamation</h3>
<ul>
<li><strong>A</strong>ccueillir : "Merci de m'avoir signalé ce problème."</li>
<li><strong>U</strong> comprendre : Reformuler pour montrer que vous avez écouté.</li>
<li><strong>R</strong>ésoudre : Proposer une solution concrète immédiatement.</li>
<li><strong>A</strong>pprendre : Noter le problème pour qu'il ne se reproduise pas.</li>
</ul>

<h3>Exercice</h3>
<p>Appelez ou écrivez à 3 anciens clients aujourd'hui. Demandez-leur simplement : "Que pouvons-nous améliorer ?" Prenez des notes. Mettez en œuvre la suggestion la plus fréquente.</p>
"""),
        ])
        Session.objects.get_or_create(
            formation=f, type_session="en_ligne",
            defaults={"nom": "Accès Libre", "places_disponibles": 100},
        )

    # =====================================================================
    # Helper
    # =====================================================================
    def _add_lecons(self, formation, lecons_data):
        for i, (titre, contenu) in enumerate(lecons_data, start=1):
            Lecon.objects.update_or_create(
                formation=formation,
                titre=titre,
                defaults={
                    "ordre": i,
                    "contenu_texte": contenu.strip(),
                    "duree_minutes": 20,
                    "est_gratuit": True,
                },
            )