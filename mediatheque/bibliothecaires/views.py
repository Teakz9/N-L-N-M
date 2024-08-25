from django.shortcuts import render
from .forms import Creationmembre
from .models import Membre


def index(request):
    return render(request, 'bibliothecaires/index.html')


def listemembres(request):
    membres = Membre.objects.all()
    return render(request, 'bibliothecaires/listemembre.html',
                  {'membres': membres})


def ajoutmembre(request):
    if request.method == 'POST':
        creationmembre = Creationmembre(request.POST)
        if creationmembre.is_valid():
            membre = Membre()
            membre.nom = creationmembre.cleaned_data['nom']
            membre.prenom = creationmembre.cleaned_data['prenom']
            membre.save()
            membres = Membre.objects.all()
            return render(request,
                          'bibliothecaires/ajoutmembre.html',
                          {'creationMembre': creationmembre})
    else:
        creationmembre = Creationmembre()
        return render(request,
                      'bibliothecaires/ajoutmembre.html',
                      {'creationMembre': creationmembre})
