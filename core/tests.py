from django.core import mail
from django.test import TestCase, override_settings

from .models import SiteSettings


class BrochurePagesTests(TestCase):
    def test_home_shows_brochure_programmes_without_unverified_claims(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        for text in ('ART ORATOIRE | PRISE DE PAROLE EN PUBLIC', 'LEADERSHIP | DEVELOPPEMENT PERSONNEL', 'INFORMATIQUE', 'LANGUES', 'AFFAIRES | ENTREPRENEURIAT'):
            self.assertContains(response, text)
        self.assertEqual(
            [pilier['description'] for pilier in response.context['piliers']],
            [
                "La plupart des professions dans la société ne peuvent s'exercer efficacement que si l'on a la maîtrise de l'Art de la parole ( Avocature, Journalisme, Enseignement, Politique, Marketing, Prédication... ), Venez apprendre !",
                "Coaching pratique sur mesure, développement d'un leadership responsable, motivationnel et fondé sur l'intelligence émotionnelle.",
                "Maîtrise des logiciels de bureautique (Word, Publisher, PowerPoint, Excel, etc.), design graphique et techniques d'imprimerie.",
                "Formation en anglais, espagnol, français et mandarin, avec une approche essentiellement pratique.",
                "Encadrement et accompagnement des jeunes vers leurs premiers pas dans l'entrepreneuriat, afin de favoriser leur autonomie et leur épanouissement.",
            ],
        )
        self.assertNotContains(response, '20 000 jeunes')
        self.assertNotContains(response, 'Certificats Reconnus')

    def test_contact_uses_brochure_phone_and_no_demo_email_form(self):
        response = self.client.get('/contact/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '+243 854 939 767')
        self.assertContains(response, 'tel:+243854939767')
        self.assertNotContains(response, 'info@atj.com')
        self.assertNotContains(response, 'Envoyer le message')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_contact_form_uses_configured_recipient(self):
        SiteSettings.objects.create(contact_email='contact@example.org')

        response = self.client.post('/contact/', {
            'nom': 'Alice',
            'email': 'alice@example.org',
            'sujet': 'Formation',
            'message': 'Je souhaite des renseignements.',
        })

        self.assertRedirects(response, '/contact/')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['contact@example.org'])
