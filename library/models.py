from django.db import models
from accounts.models import CustomUser
import os
import zipfile
import xml.etree.ElementTree as ET
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
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # 2. Génération de la couverture si absente
        if self.fichier and not self.image:
            try:
                # --- PDF LOGIC ---
                if self.fichier.name.lower().endswith('.pdf') and convert_from_bytes:
                    images = None
                    try:
                        if self.fichier.path and os.path.exists(self.fichier.path) and convert_from_path:
                            images = convert_from_path(self.fichier.path, first_page=1, last_page=1)
                    except Exception as e:
                        print(f"Cover gen check path failed: {e}")

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
                        if cover.mode != 'RGB':
                            cover = cover.convert('RGB')
                        
                        buffer = BytesIO()
                        cover.save(buffer, format="JPEG", quality=85)
                        self._save_cover_data(buffer.getvalue(), 'jpg')

                # --- EPUB LOGIC ---
                elif self.fichier.name.lower().endswith('.epub'):
                     try:
                        if self.fichier.path and os.path.exists(self.fichier.path):
                            with zipfile.ZipFile(self.fichier.path, 'r') as z:
                                # Find OPF Path
                                opf_path = None
                                try:
                                    with z.open('META-INF/container.xml') as f:
                                        root = ET.fromstring(f.read())
                                        for rootfile in root.findall('.//{*}rootfile'):
                                            opf_path = rootfile.get('full-path')
                                            if opf_path: break
                                except: pass
                                
                                if not opf_path:
                                    # Fallback: find any .opf
                                    opf_path = next((n for n in z.namelist() if n.endswith('.opf')), None)
                                
                                if opf_path:
                                    with z.open(opf_path) as f:
                                        opf_content = f.read()
                                        root = ET.fromstring(opf_content)
                                        
                                        # Find cover ID
                                        cover_id = None
                                        # Strategy A: <meta name="cover" content="...">
                                        for meta in root.findall('.//{*}meta'):
                                            if meta.get('name') == 'cover':
                                                cover_id = meta.get('content')
                                                break
                                        
                                        # Strategy B: item properties="cover-image"
                                        if not cover_id:
                                            for item in root.findall('.//{*}manifest/{*}item'):
                                                props = item.get('properties', '') if item.get('properties') else ''
                                                if 'cover-image' in props.split():
                                                    cover_id = item.get('id')
                                                    break
                                        
                                        if cover_id:
                                            # Find HREF
                                            href = None
                                            for item in root.findall('.//{*}manifest/{*}item'):
                                                if item.get('id') == cover_id:
                                                    href = item.get('href')
                                                    break
                                            
                                            if href:
                                                # Resolve path
                                                opf_dir = os.path.dirname(opf_path)
                                                image_path = os.path.join(opf_dir, href).replace('\\', '/')
                                                image_data = None
                                                try:
                                                    image_data = z.read(image_path)
                                                except KeyError:
                                                    # Try searching basics
                                                    target = os.path.basename(href)
                                                    for n in z.namelist():
                                                        if n.endswith(target):
                                                            image_data = z.read(n)
                                                            break
                                                
                                                if image_data:
                                                    self._save_cover_data(image_data, 'jpg')

                     except Exception as e:
                         print(f"EPUB cover extraction failed: {e}")

            except Exception as e:
                print(f"Error generating cover for {self.titre}: {e}")

    def _save_cover_data(self, data, ext):
        fname = os.path.basename(self.fichier.name)
        base, _ = os.path.splitext(fname)
        cover_name = f"{base}_cover.{ext}"
        self.image.save(cover_name, ContentFile(data), save=False)
        Livre.objects.filter(pk=self.pk).update(image=self.image)

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
