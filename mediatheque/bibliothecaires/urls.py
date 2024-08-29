from django.urls import path
from . import views

urlpatterns = [
    path('', views.connexion, name="connexion"),
    path('deconnexion/', views.deconnexion, name="deconnexion"),
    path('index/', views.index, name='bibliothecaires_index'),
    path('ajoutmembre/', views.ajout_membre, name="ajout_membre"),
    path('listemembre/', views.liste_membres, name="liste_membre"),
    path('modifiermembre/<int:id>/', views.modifier_membre, name="modifier_membre"),
    path('supprimermembre/<int:id>/', views.supprimer_membre, name="supprimer_membre"),
    path('listemedia/', views.liste_media, name="liste_media"),
    path('ajoutmedia/', views.ajout_media, name="ajout_media"),
    path('creeremprunt/', views.creer_emprunt, name="creer_emprunt"),
]
