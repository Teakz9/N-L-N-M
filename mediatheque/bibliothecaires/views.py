from django.shortcuts import get_object_or_404, render
from .forms import Creationmembre, Modifiermembre
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


def modifiermembre(request, id):
    membre = get_object_or_404(Membre, pk=id)
    if request.method == 'POST':
        modifier_membre = Modifiermembre(request.POST, instance=membre)
        if modifier_membre.is_valid():
            modifier_membre.save()
            membres = Membre.objects.all()
            return render(request, 'bibliothecaires/listemembre.html',
                          {'membres': membres})
    else:
        modifier_membre = Modifiermembre(instance=membre)
        return render(request,
                      'bibliothecaires/modifiermembre.html',
                      {'modifiermembre': modifier_membre}
                      )
