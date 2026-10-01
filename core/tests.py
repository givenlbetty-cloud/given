from django.core import mail
from django.test import TestCase, override_settings

from .models import SiteSettings


class BrochurePagesTests(TestCase):
    def test_home_shows_brochure_programmes_without_unverified_claims(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        for text in ('Art oratoire', 'Leadership', 'Informatique', 'Langues', 'Affaires et entrepreneuriat'):
            self.assertContains(response, text)
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
