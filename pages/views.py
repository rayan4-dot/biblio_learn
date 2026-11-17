from django.shortcuts import render
from .forms import ContactForm


def accueil(request):
    contexte = {
        "nom_projet": "BiblioLearn",
        "modules": ["Catalogue", "Comptes et rôles", "Emprunts", "Mini-cours"],
        "nb_ressources": 0,
    }
    return render(request, "pages/accueil.html", contexte)


def a_propos(request):
    equipe = [
        {"nom": "Rayan Mansour", "role": "Chef de projet & Développeur Backend"},
        {"nom": "Sara Alami", "role": "Développeuse Frontend & UI/UX"},
        {"nom": "Youssef Bennani", "role": "Développeur Fullstack"},
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
