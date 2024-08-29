from django.shortcuts import render
import django


def home(request):
    return render(request, 'home.html')


print(django.get_version())
