from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='bibliothecaires_index'),
    path('ajoutmembre/', views.ajoutmembre, name="ajout_membre"),
    path('listemembre/', views.listemembres, name="liste_membre"),
    path('modifiermembre/<int:id>/', views.modifiermembre, name="modifier_membre"),
    path('listemedia/', views.liste_media, name="liste_media"),
]
