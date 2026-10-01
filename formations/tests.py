from django.test import TestCase
from django.urls import reverse

from core.brochure import PILIERS
from .models import Formation


class PublicFormationPresentationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.formation = Formation.objects.create(
            titre='Atelier de prise de parole',
            categorie='art_oratoire',
            description='Une présentation complète de cette formation ATJ.',
            est_publie=True,
        )

    def test_every_category_shows_its_brochure_text_and_photo(self):
        for pilier in PILIERS:
            with self.subTest(categorie=pilier['code']):
                response = self.client.get(reverse('formations:liste'), {'categorie': pilier['code']})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context['pilier'], pilier)
                self.assertContains(response, pilier['image'])

    def test_catalog_shows_all_brochure_domains_without_published_courses(self):
        self.formation.est_publie = False
        self.formation.save(update_fields=['est_publie'])

        response = self.client.get(reverse('formations:liste'))

        self.assertEqual(response.status_code, 200)
        for pilier in PILIERS:
            self.assertContains(response, pilier['titre'])
            self.assertContains(response, pilier['image'])
        self.assertNotContains(response, 'Aucune formation trouvée.')

    def test_public_presentation_shows_photo_and_full_description(self):
        response = self.client.get(reverse('formations:detail_formation', args=[self.formation.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.formation.titre)
        self.assertContains(response, self.formation.description)
        self.assertContains(response, self.formation.pilier['image'])
        self.assertContains(response, 'Selon le dépliant ATJ')

    def test_unpublished_formation_has_no_public_presentation(self):
        self.formation.est_publie = False
        self.formation.save(update_fields=['est_publie'])

        response = self.client.get(reverse('formations:detail_formation', args=[self.formation.id]))

        self.assertEqual(response.status_code, 404)
