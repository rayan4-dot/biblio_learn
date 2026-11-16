from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, request


def accueil(request):
    contexte = {
        "nom_projet": "BiblioLearn",
        "modules": ["Catalogue", "Comptes et rôles", "Emprunts", "Mini-cours"],
    }
    return render(request, "pages/accueil.html", contexte)