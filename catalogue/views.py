from django.shortcuts import get_object_or_404, render
from .models import Ressource


def liste(request):
    ressources = Ressource.objects.select_related("categorie")
    return render(request, "catalogue/liste.html", {"ressources": ressources})


def detail(request, pk):
    ressource = get_object_or_404(Ressource, pk=pk)
    return render(request, "catalogue/detail.html", {"ressource": ressource})
