"""Textes du dépliant ATJ et photos associées aux cinq domaines."""

MISSION = (
    "L'Académie Tremplin de la Jeunesse a pour mission de former et d'accompagner "
    "les jeunes dans leur développement personnel et professionnel. À travers les "
    "programmes de formation en leadership, en prise de parole en public, en "
    "informatique, en langues et en affaires."
)

VISION = (
    "Nous visons à préparer les Jeunes à relever les défis du monde moderne et à "
    "devenir des acteurs de changement dans leur communauté."
)

PILIERS = [
    {
        'code': 'art_oratoire',
        'titre': 'ART ORATOIRE | PRISE DE PAROLE EN PUBLIC',
        'icone': 'bi-mic-fill',
        'image': 'img/atj/gm1-5845.jpeg',
        'image_alt': "Participant s'exprimant au microphone lors d'une activité de l'ATJ",
        'description': "La plupart des professions dans la société ne peuvent s'exercer efficacement que si l'on a la maîtrise de l'Art de la parole ( Avocature, Journalisme, Enseignement, Politique, Marketing, Prédication... ), Venez apprendre !",
    },
    {
        'code': 'leadership',
        'titre': 'LEADERSHIP | DEVELOPPEMENT PERSONNEL',
        'icone': 'bi-people-fill',
        'image': 'img/atj/gm1-5847.jpeg',
        'image_alt': "Intervenant prenant la parole lors d'une activité de l'ATJ",
        'description': "Coaching pratique sur mesure, développement d'un leadership responsable, motivationnel et fondé sur l'intelligence émotionnelle.",
    },
    {
        'code': 'informatique',
        'titre': 'INFORMATIQUE',
        'icone': 'bi-laptop',
        'image': 'img/atj/atj-atelier-informatique.jpeg',
        'image_alt': "Deux participantes de l'ATJ travaillant sur un ordinateur",
        'description': "Maîtrise des logiciels de bureautique (Word, Publisher, PowerPoint, Excel, etc.), design graphique et techniques d'imprimerie.",
    },
    {
        'code': 'langues',
        'titre': 'LANGUES',
        'icone': 'bi-translate',
        'image': 'img/atj/atj-groupe.jpeg',
        'image_alt': "Groupe de participants de l'ATJ avec leurs certificats",
        'description': "Formation en anglais, espagnol, français et mandarin, avec une approche essentiellement pratique.",
    },
    {
        'code': 'affaires',
        'titre': 'AFFAIRES | ENTREPRENEURIAT',
        'icone': 'bi-briefcase-fill',
        'image': 'img/atj/gm1-5853.jpeg',
        'image_alt': "Membre de l'ATJ participant à une réunion",
        'description': "Encadrement et accompagnement des jeunes vers leurs premiers pas dans l'entrepreneuriat, afin de favoriser leur autonomie et leur épanouissement.",
    },
]

PILIER_PAR_CODE = {pilier['code']: pilier for pilier in PILIERS}
