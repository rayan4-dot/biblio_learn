from django.shortcuts import get_object_or_404, render
from .models import Ressource


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
