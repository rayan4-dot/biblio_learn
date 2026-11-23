from django.shortcuts import render
from catalogue.models import Auteur, Categorie, Ressource
from .forms import ContactForm


def accueil(request):
    contexte = {
        "nom_projet": "BiblioLearn",
        "modules": [
            {
                "nom": "Catalogue Universitaire",
                "desc": "Index exhaustif de livres, thèses, cours et articles scientifiques classés et filtrables.",
                "icone": "book-open",
                "tag": "Recherche avancée",
                "lien": "catalogue:liste",
            },
            {
                "nom": "Comptes & Rôles",
                "desc": "Espace dédié pour étudiants, enseignants et chercheurs avec gestion personnalisée.",
                "icone": "user-check",
                "tag": "Authentification",
                "lien": "admin:index",
            },
            {
                "nom": "Système d'Emprunts",
                "desc": "Suivi en temps réel de la disponibilité et réservation immédiate des exemplaires physiques.",
                "icone": "calendar",
                "tag": "Disponibilité",
                "lien": "catalogue:liste",
            },
            {
                "nom": "Mini-cours & Tutoriels",
                "desc": "Modules d'auto-formation interactifs conçus par le corps professoral de l'ESMA.",
                "icone": "award",
                "tag": "Pédagogie",
                "lien": "pages:a_propos",
            },
        ],
        "nb_ressources": Ressource.objects.count(),
        "nb_categories": Categorie.objects.count(),
        "nb_auteurs": Auteur.objects.count(),
        "categories_list": Categorie.objects.all(),
        "dernieres_parutions": (
            Ressource.objects.select_related("categorie")
            .prefetch_related("auteurs")
            .order_by("-annee")[:3]
        ),
    }
    return render(request, "pages/accueil.html", contexte)


def a_propos(request):
    equipe = [
        {
            "nom": "Rayan Mansour",
            "role": "Chef de projet & Développeur Backend",
            "initiales": "RM",
            "desc": "Architecture Django, conception ORM et optimisation des flux de données.",
        },
        {
            "nom": "Sara Alami",
            "role": "Développeuse Frontend & UI/UX",
            "initiales": "SA",
            "desc": "Design System haut de gamme, expérience utilisateur et ergonomie visuelle.",
        },
        {
            "nom": "Youssef Bennani",
            "role": "Développeur Fullstack",
            "initiales": "YB",
            "desc": "Intégration des composants réactifs, administration et déploiement continu.",
        },
    ]
    return render(
        request,
        "pages/a_propos.html",
        {
            "equipe": equipe,
            "membres": equipe,
        },
    )


def contact(request):
    message_confirmation = None
    nom = None
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data["nom"]
            message_confirmation = f"Merci {nom}, votre message a bien été reçu"
    else:
        form = ContactForm()

    return render(
        request,
        "pages/contact.html",
        {
            "form": form,
            "message_confirmation": message_confirmation,
            "nom": nom,
        },
    )
