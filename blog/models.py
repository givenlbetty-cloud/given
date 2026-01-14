from django.db import models

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)

    def __str__(self):
        return self.titre

class Ressource(models.Model):
    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='ressources/', blank=True, null=True)
    lien_video = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.titre

class Event(models.Model):
    titre = models.CharField(max_length=200)
    date = models.DateTimeField()
    lieu = models.CharField(max_length=200)
    lien_inscription = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titre
