from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='membres_home'),
    path('listemedia', views.liste_media_membres, name='liste_media')
]