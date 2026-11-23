from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Auteur, Categorie, Ressource


def liste(request):
    ressources = Ressource.objects.select_related("categorie").prefetch_related(
        "auteurs"
    )
    q = request.GET.get("q", "").strip()
    type_choisi = request.GET.get("type", "")
    categorie_choisie = request.GET.get("categorie", "")
    dispo = request.GET.get("dispo") == "1"

    if q:
        ressources = ressources.filter(
            Q(titre__icontains=q) | Q(auteurs__nom__icontains=q)
        ).distinct()
    if type_choisi:
        ressources = ressources.filter(type_ressource=type_choisi)
    if categorie_choisie.isdigit():
        ressources = ressources.filter(categorie_id=categorie_choisie)
    if dispo:
        ressources = ressources.filter(disponible=True)

    contexte = {
        "ressources": ressources,
        "types": Ressource.TYPE_CHOIX,
        "categories": Categorie.objects.all(),
        "filtres": {
            "q": q,
            "type": type_choisi,
            "categorie": categorie_choisie,
            "dispo": dispo,
        },
    }
    return render(request, "catalogue/liste.html", contexte)


def detail(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    return render(request, "catalogue/detail.html", {"ressource": ressource})


def par_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    ressources = categorie.ressources.select_related("categorie").prefetch_related(
        "auteurs"
    )
    contexte = {
        "ressources": ressources,
        "types": Ressource.TYPE_CHOIX,
        "categories": Categorie.objects.all(),
        "filtres": {},
        "categorie": categorie,
    }
    return render(request, "catalogue/liste.html", contexte)


def par_auteur(request, pk):
    auteur = get_object_or_404(Auteur, pk=pk)
    ressources = auteur.ressources.select_related("categorie").prefetch_related(
        "auteurs"
    )
    contexte = {
        "ressources": ressources,
        "types": Ressource.TYPE_CHOIX,
        "categories": Categorie.objects.all(),
        "filtres": {},
        "auteur": auteur,
    }
    return render(request, "catalogue/liste.html", contexte)


def categories(request):
    return render(
        request, "catalogue/categories.html", {"categories": Categorie.objects.all()}
    )
