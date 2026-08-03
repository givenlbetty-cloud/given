"""
Génère les couvertures (1ère page PDF) pour tous les livres qui n'en ont pas.
Usage : python manage.py generate_covers
"""
from django.core.management.base import BaseCommand
from library.models import Livre
from io import BytesIO
from django.core.files.base import ContentFile

try:
    from pdf2image import convert_from_bytes
except ImportError:
    convert_from_bytes = None


class Command(BaseCommand):
    help = 'Génère les couvertures manquantes à partir de la 1ère page du PDF'

    def handle(self, *args, **options):
        if not convert_from_bytes:
            self.stderr.write('pdf2image non installé. Installez poppler-utils + pdf2image.')
            return

        livres = Livre.objects.filter(image__isnull=True, fichier__isnull=False)
        updated = 0

        for livre in livres:
            if not livre.fichier.name.lower().endswith('.pdf'):
                continue

            try:
                livre.fichier.open('rb')
                content = livre.fichier.read()
                livre.fichier.close()

                if not content:
                    continue

                images = convert_from_bytes(content, first_page=1, last_page=1)
                if images:
                    buffer = BytesIO()
                    img = images[0].convert('RGB')
                    img.save(buffer, format='JPEG', quality=85)
                    livre.image.save('cover.jpg', ContentFile(buffer.getvalue()), save=True)
                    updated += 1
                    self.stdout.write(f'✅ Couverture générée : {livre.titre}')
            except Exception as e:
                self.stderr.write(f'❌ Erreur {livre.titre}: {e}')

        self.stdout.write(self.style.SUCCESS(f'{updated} couverture(s) générée(s)'))