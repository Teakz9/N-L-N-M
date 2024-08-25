from django.db import models


class Membre(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
