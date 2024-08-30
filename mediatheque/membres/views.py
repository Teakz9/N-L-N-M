from django.shortcuts import render
from bibliothecaires.views import liste_media as bibliothecaires_liste_media

def index(request):
    return render(request, 'membres/index.html')


def liste_media_membres(request):
    return bibliothecaires_liste_media(request)