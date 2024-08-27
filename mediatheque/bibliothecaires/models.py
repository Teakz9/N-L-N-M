from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Membre(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Media(models.Model):
    TYPE_CHOICES = [
        ('Livre', 'Livre'),
        ('CD', 'CD'),
        ('DVD', 'DVD'),
    ]

    titre = models.CharField(max_length=150)
    auteur = models.CharField(max_length=150)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titre} ({self.get_type_display()}) par {self.auteur}"


class JeuDePlateau(models.Model):
    nom = models.CharField(max_length=150)
    auteur = models.CharField(max_length=150)

    def __str__(self):
        return f"Jeu de plateau: {self.nom} par {self.auteur}"


class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.membre.emprunt_set.filter(date_retour__isnull=True).count() >= 3:
            raise ValidationError("Ce membre a déjà 3 emprunts actifs !")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.media.titre} emprunté par {self.membre.nom} {self.membre.prenom}"
