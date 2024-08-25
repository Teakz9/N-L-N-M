from django import forms
from .models import Membre


class Creationmembre(forms.Form):
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)


class Modifiermembre(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom']
