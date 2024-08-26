from django.db import models


class Membre(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)


class Media(models.Model):
    TYPE_CHOICES = [
        ('Livre', 'Livre'),
        ('CD', 'CD'),
        ('DVD', 'DVD'),
        ('Jeu de plateau', 'Jeu de plateau'),
    ]

    titre = models.CharField(max_length=150)
    auteur = models.CharField(max_length=150)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    disponible = models.BooleanField(default=True)
