from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import Creationmembre, Modifiermembre, Creationmedia, Creationjeudeplateau, Empruntform
from .models import Membre, Media, JeuDePlateau, Emprunt


def connexion(request):
    if request.method == 'POST':
        username = request.POST['utilisateur']
        password = request.POST['motdepasse']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('bibliothecaires_index')
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect')

    return render(request, 'bibliothecaires/connexion.html')


@login_required
def index(request):
    return render(request, 'bibliothecaires/index.html')


def deconnexion(request):
    logout(request)
    return redirect('connexion')


def liste_membres(request):
    membres = Membre.objects.all().prefetch_related('emprunt_set__media')
    return render(request, 'bibliothecaires/listemembre.html',
                  {'membres': membres})


def ajout_membre(request):
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


def modifier_membre(request, id):
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


def supprimer_membre(request, id):
    membre = get_object_or_404(Membre, pk=id)
    membre.delete()
    return redirect('liste_membre')


def liste_media(request):
    medias = Media.objects.all().order_by('type')
    jeux_de_plateau = JeuDePlateau.objects.all()

    medias_by_type = {}
    for media in medias:
        if media.type not in medias_by_type:
            medias_by_type[media.type] = []
        medias_by_type[media.type].append(media)

    return render(request, 'bibliothecaires/listemedia.html', {
        'medias_by_type': medias_by_type,
        'jeux_de_plateau': jeux_de_plateau})


def ajout_media(request):
    if request.method == 'POST':
        media_form = Creationmedia(request.POST)
        jeu_form = Creationjeudeplateau(request.POST)

        if media_form.is_valid():
            media_form.save()
            return redirect('liste_media')

        if jeu_form.is_valid():
            jeu_form.save()
            return redirect('liste_media')
    else:
        media_form = Creationmedia()
        jeu_form = Creationjeudeplateau()

    return render(request, 'bibliothecaires/ajoutmedia.html', {
        'media_form': media_form,
        'jeu_form': jeu_form,
    })


def creer_emprunt(request):
    if request.method == 'POST':
        form = Empruntform(request.POST)
        if form.is_valid():
            emprunt = form.save(commit=False)
            membre = emprunt.membre

            emprunts_retard = membre.emprunt_set.filter(date_retour__isnull=True,
                                                        date_emprunt__lt=timezone.now() - timedelta(days=7))
            if emprunts_retard.exists():
                messages.error(request, "Ce membre a un ou plusieurs retards.")
                return redirect('creer_emprunt')

            if membre.emprunt_set.filter(date_retour__isnull=True).count() >= 3:
                messages.error(request, "Ce membre a déjà 3 emprunts actifs.")
                return redirect('creer_emprunt')

            emprunt.date_retour = emprunt.date_emprunt + timedelta(days=7)

            media = emprunt.media
            media.disponible = False
            media.save()
            emprunt.save()

            messages.success(request, 'Emprunt validé.')
            return redirect('liste_membre')
    else:
        form = Empruntform()

    return render(request, 'bibliothecaires/creeremprunt.html', {'form': form})
