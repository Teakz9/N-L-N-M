import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mediatheque.settings'
django.setup()
import pytest
from django.urls import reverse
from django.test import Client
from bibliothecaires.models import Membre, Media, Emprunt
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestViews:
    def setup_method(self):
        self.client = Client()

    def test_liste_membres_view(self):
        Membre.objects.create(nom="Test", prenom="User")
        response = self.client.get(reverse('liste_membre'))
        assert response.status_code == 200
        assert 'bibliothecaires/listemembre.html' in [t.name for t in response.templates]
        assert "Test" in response.content.decode()

    def test_ajout_membre_view(self):
        response = self.client.post(reverse('ajout_membre'), {'nom': 'Doe', 'prenom': 'John'})
        assert response.status_code == 200
        assert Membre.objects.filter(nom='Doe', prenom='John').exists()

    def test_modifier_membre_view(self):
        membre = Membre.objects.create(nom='Doe', prenom='John')
        response = self.client.post(reverse('modifier_membre', args=[membre.id]),
                                    {'nom': 'Bezos', 'prenom': 'Jeff'})
        assert response.status_code == 200
        membre.refresh_from_db()
        assert membre.nom == 'Bezos'

    def test_supprimer_membre_view(self):
        membre = Membre.objects.create(nom='Doe', prenom='John')
        response = self.client.post(reverse('supprimer_membre', args=[membre.id]))
        assert response.status_code == 302
        assert not Membre.objects.filter(id=membre.id).exists()

    def test_creer_emprunt_view(self):
        membre = Membre.objects.create(nom='Doe', prenom='John')
        media = Media.objects.create(titre='Titre', auteur='Auteur', type='DVD')
        response = self.client.post(reverse('creer_emprunt'), {'membre': membre.id, 'media': media.id})
        assert response.status_code == 302
        assert Emprunt.objects.filter(membre=membre, media=media).exists()

    def test_creer_emprunt_limite(self):
        membre = Membre.objects.create(nom='Doe', prenom='John')
        media = Media.objects.create(titre='Titre', auteur='Auteur', type='DVD')
        for _ in range(3):
            Emprunt.objects.create(membre=membre, media=media)
        response = self.client.post(reverse('creer_emprunt'), {'membre': membre.id, 'media': media.id})
        assert response.status_code == 302
        assert Emprunt.objects.filter(membre=membre).count() == 3

    def test_creer_emprunt_retard(self):
        membre = Membre.objects.create(nom='Doe', prenom='John')
        media = Media.objects.create(titre='Titre', auteur='Auteur', type='DVD')
        Emprunt.objects.create(membre=membre, media=media, date_emprunt=timezone.now() - timedelta(days=7))
        response = self.client.post(reverse('creer_emprunt'), {'membre': membre.id, 'media': media.id})
        assert response.status_code == 302
        assert "Ce membre contient déjà un ou plusieurs retards" in response.content.decode()
