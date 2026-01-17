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
        # Auto-generate cover from PDF if no image is provided
        if self.fichier and not self.image and convert_from_bytes:
            try:
                if self.fichier.name.lower().endswith('.pdf'):
                    images = None
                    
                    # 1. Try from path (existing file on disk) -> More reliable for large files
                    try:
                        # Check path existence safely (might throw error if not saved yet)
                        path = self.fichier.path 
                        if path and os.path.exists(path) and convert_from_path:
                             images = convert_from_path(path, first_page=1, last_page=1)
                    except Exception:
                        pass
                    
                    # 2. Try from content (uploaded file in memory) -> For new uploads
                    if not images:
                        content = None
                        try:
                            # Handle different file states (open/closed/memory)
                            if hasattr(self.fichier, 'closed') and not self.fichier.closed:
                                if hasattr(self.fichier, 'seek'):
                                    self.fichier.seek(0)
                                content = self.fichier.read()
                                if hasattr(self.fichier, 'seek'):
                                    self.fichier.seek(0)
                            else:
                                with self.fichier.open('rb') as f:
                                    content = f.read()
                        except Exception:
                            # Last resort: try reading file path directly if open() failed
                            try:
                                if self.fichier.path and os.path.exists(self.fichier.path):
                                    with open(self.fichier.path, 'rb') as f:
                                        content = f.read()
                            except:
                                pass
                        
                        if content:
                            images = convert_from_bytes(content, first_page=1, last_page=1)

                    if images:
                        cover = images[0]
                        buffer = BytesIO()
                        # Convert to RGB to avoid issues with CMYK PDFs considering we save as JPEG
                        if cover.mode != 'RGB':
                            cover = cover.convert('RGB')
                        
                        cover.save(buffer, format="JPEG", quality=85)
                        val = buffer.getvalue()
                        
                        fname = os.path.basename(self.fichier.name)
                        base, _ = os.path.splitext(fname)
                        cover_name = f"{base}_cover.jpg"
                        
                        self.image.save(cover_name, ContentFile(val), save=False)
            except Exception as e:
                print(f"Error generating cover for {self.titre}: {e}")
        
        super().save(*args, **kwargs)

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
