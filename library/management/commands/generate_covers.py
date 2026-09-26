"""Generate missing book covers from the first page of PDF files."""
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from library.models import Livre, convert_from_bytes


class Command(BaseCommand):
    help = "Genere les couvertures absentes depuis la premiere page des PDF"

    def handle(self, *args, **options):
        if not convert_from_bytes:
            raise CommandError("pdf2image est absent. Installez pdf2image et Poppler.")

        books = Livre.objects.filter(fichier__isnull=False).exclude(fichier="").filter(
            Q(image__isnull=True) | Q(image="")
        )
        updated = 0

        for book in books:
            if not book.fichier.name.lower().endswith(".pdf"):
                continue
            try:
                if book.generate_cover_from_pdf():
                    updated += 1
                    self.stdout.write(f"Couverture generee : {book.titre}")
            except Exception as error:
                self.stderr.write(f"Erreur pour {book.titre}: {error}")

        self.stdout.write(self.style.SUCCESS(f"{updated} couverture(s) generee(s)"))
