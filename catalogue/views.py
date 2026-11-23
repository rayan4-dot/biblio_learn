from django.shortcuts import get_object_or_404, render
from .models import Categorie, Ressource


def liste(request):
    q = request.GET.get("q", "").strip()
    ressources = Ressource.objects.select_related("categorie")
    if q:
        ressources = ressources.filter(titre__icontains=q)
    return render(
        request,
        "catalogue/liste.html",
        {
            "ressources": ressources,
            "q": q,
        },
    )


def detail(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    return render(request, "catalogue/detail.html", {"ressource": ressource})


def categories(request):
    categories = Categorie.objects.all()
    return render(
        request,
        "catalogue/categories.html",
        {
            "categories": categories,
        },
    )


def par_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    ressources = categorie.ressources.all()
    q = request.GET.get("q", "").strip()
    if q:
        ressources = ressources.filter(titre__icontains=q)
    return render(
        request,
        "catalogue/liste.html",
        {
            "ressources": ressources,
            "categorie": categorie,
            "q": q,
        },
    )


def par_auteur(request, pk):
    auteur = get_object_or_404(Auteur, pk=pk)
    ressources = auteur.ressources.select_related("categorie")
    return render(
        request,
        "catalogue/liste.html",
        {"ressources": ressources, "auteur": auteur},
    )
