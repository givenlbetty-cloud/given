from django.db import models
from accounts.models import CustomUser
import os
from io import BytesIO
from django.core.files.base import ContentFile
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
        # 1. Sauvegarde initiale pour s'assurer que le fichier est sur le disque si possible
        # Attention à la récursion si on rappelle save()
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # 2. Génération de la couverture si absente
        if self.fichier and not self.image and convert_from_bytes:
            try:
                images = None
                # Si le fichier est un PDF
                if self.fichier.name.lower().endswith('.pdf'):
                    # Option A: Essayer depuis le chemin disque (maintenant qu'on a fait super().save())
                    try:
                        if self.fichier.path and os.path.exists(self.fichier.path) and convert_from_path:
                            images = convert_from_path(self.fichier.path, first_page=1, last_page=1)
                    except Exception as e:
                        print(f"Cover gen check path failed: {e}")

                    # Option B: Essayer depuis le contenu (si le fichier n'est pas accessible via path)
                    if not images:
                        try:
                            self.fichier.open('rb')
                            content = self.fichier.read()
                            if content:
                                images = convert_from_bytes(content, first_page=1, last_page=1)
                        except Exception as e:
                            print(f"Cover gen check content failed: {e}")
                        finally:
                            self.fichier.close()

                    if images:
                        cover = images[0]
                        # Conversion RGB pour compatibilité JPEG
                        if cover.mode != 'RGB':
                            cover = cover.convert('RGB')
                        
                        buffer = BytesIO()
                        cover.save(buffer, format="JPEG", quality=85)
                        val = buffer.getvalue()
                        
                        fname = os.path.basename(self.fichier.name)
                        base, _ = os.path.splitext(fname)
                        cover_name = f"{base}_cover.jpg"
                        
                        # Sauvegarde de l'image
                        # save=False pour éviter une boucle infinie de super().save()
                        # Mais il faut sauvegarder le champ.
                        self.image.save(cover_name, ContentFile(val), save=False)
                        
                        # On force l'update SQL uniquement pour le champ image pour éviter récursion complète
                        Livre.objects.filter(pk=self.pk).update(image=self.image)
            except Exception as e:
                print(f"Error generating cover for {self.titre}: {e}")

    def is_free(self):
        # Modification : Toutes les ressources sont gratuites pour les membres
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
