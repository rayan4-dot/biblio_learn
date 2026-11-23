from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from .models import Auteur, Categorie, Ressource

PAR_PAGE = 3


def paginer(request, ressources):
    """Découpe le QuerySet en pages et prépare les liens de navigation."""
    paginator = Paginator(ressources, PAR_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return page_obj, params.urlencode()


def liste(request):
    ressources = Ressource.objects.select_related("categorie").prefetch_related(
        "auteurs"
    )
    q = request.GET.get("q", "").strip()
    type_choisi = request.GET.get("type", "")
    categorie_choisie = request.GET.get("categorie", "")
    dispo = request.GET.get("dispo") == "1"
    tri = request.GET.get("tri", "")

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

    TRIS = {"titre": "titre", "recent": "-annee", "ancien": "annee"}
    if tri in TRIS:
        ressources = ressources.order_by(TRIS[tri])

    page_obj, querystring = paginer(request, ressources)
    contexte = {
        "page_obj": page_obj,
        "querystring": querystring,
        "types": Ressource.TYPE_CHOIX,
        "categories": Categorie.objects.all(),
        "filtres": {
            "q": q,
            "type": type_choisi,
            "categorie": categorie_choisie,
            "dispo": dispo,
            "tri": tri,
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
    page_obj, querystring = paginer(request, ressources)
    contexte = {
        "page_obj": page_obj,
        "querystring": querystring,
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
    page_obj, querystring = paginer(request, ressources)
    contexte = {
        "page_obj": page_obj,
        "querystring": querystring,
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


def auteurs(request):
    liste_auteurs = Auteur.objects.annotate(nb=Count("ressources"))
    return render(request, "catalogue/auteurs.html", {"auteurs": liste_auteurs})
