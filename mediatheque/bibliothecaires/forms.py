from django import forms
from .models import Membre, Media, JeuDePlateau


class Creationmembre(forms.Form):
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)


class Modifiermembre(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom']


class Creationmedia(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'auteur', 'type', 'disponible']


class Creationjeudeplateau(forms.ModelForm):
    class Meta:
        model = JeuDePlateau
        fields = ['nom', 'auteur']