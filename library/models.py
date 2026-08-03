from django.db import models
from accounts.models import CustomUser
import os
from io import BytesIO
from django.core.files.base import ContentFile

# pdf2image - nécessite poppler-utils installé sur le serveur
try:
    from pdf2image import convert_from_bytes, convert_from_path
except ImportError:
    convert_from_bytes = None
    convert_from_path = None


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)
    CATEGORIES = [
        ('dev', 'Développement'),
        ('business', 'Business & Marketing'),
        ('design', 'Design & Art'),
        ('science', 'Science & Tech'),
        ('other', 'Autre'),
    ]
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    description = models.TextField()
    image = models.ImageField(upload_to='livres_images/', blank=True, null=True)
    fichier = models.FileField(upload_to='livres_fichiers/', help_text="PDF ou EPUB")
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, help_text="0.00 pour gratuit")
    date_creation = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Génère la couverture automatiquement (1ère page PDF) si absente."""
        super().save(*args, **kwargs)

        # Condition stricte : fichier présent + pas d'image + pdf2image disponible
        if not self.fichier or self.image or not convert_from_bytes:
            return

        # Tenter uniquement sur les PDF
        if not self.fichier.name.lower().endswith('.pdf'):
            return

        try:
            # Lire le contenu du fichier
            self.fichier.open('rb')
            content = self.fichier.read()
            self.fichier.close()

            if not content:
                return

            # Extraire la 1ère page en image
            images = convert_from_bytes(content, first_page=1, last_page=1)
            if images:
                cover = images[0]
                if cover.mode != 'RGB':
                    cover = cover.convert('RGB')
                buffer = BytesIO()
                cover.save(buffer, format='JPEG', quality=85)

                # Sauvegarder l'image de couverture
                fname = os.path.basename(self.fichier.name)
                base, _ = os.path.splitext(fname)
                cover_name = f'{base}_cover.jpg'
                self.image.save(cover_name, ContentFile(buffer.getvalue()), save=False)
                Livre.objects.filter(pk=self.pk).update(image=self.image)
        except Exception:
            pass  # Silencieux : la couverture auto est un bonus, pas un blocage

    def is_free(self):
        return True

    def __str__(self):
        return self.titre


class AchatLivre(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_achat = models.DateTimeField(auto_now_add=True)
    derniere_page_lue = models.IntegerField(default=1)
    est_termine = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.livre.titre}"


class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    contenu = models.TextField()
    page_reference = models.IntegerField(null=True, blank=True, help_text="Numéro de page associé à la note")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note de {self.user.username} sur {self.livre.titre}"


class Avis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='avis')
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.user.username} sur {self.livre.titre}"


class Favori(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favoris')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='favoris_users')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'livre')

    def __str__(self):
        return f"{self.user.username} aime {self.livre.titre}"