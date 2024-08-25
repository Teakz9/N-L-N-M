from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='bibliothecaires_index'),
    path('ajoutmembre/', views.ajoutmembre, name="ajout_membre"),
    path('listemembre/', views.listemembres, name="liste_membre"),
]
