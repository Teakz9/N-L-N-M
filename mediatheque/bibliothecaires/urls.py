from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='bibliothecaires_index'),
]
