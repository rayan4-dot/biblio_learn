from catalogue.models import Auteur, Ressource

liens = {
    "Python pour tous": ["Amrani"],
    "Apprendre Django pas à pas": ["Amrani", "Benali"],
    "Introduction aux bases de données": ["Benali"],
    "Algèbre linéaire": ["El Idrissi"],
    "Probabilités et statistiques": ["El Idrissi", "Tazi"],
    "Les graphes en pratique": ["Tazi"],
    "Grammaire française": ["Chraibi"],
    "Histoire de la littérature arabe": ["Chraibi"],
}

for titre, noms in liens.items():
    ressource = Ressource.objects.get(titre=titre)
    ressource.auteurs.set(Auteur.objects.filter(nom__in=noms))
    print(titre, "->", ressource.auteurs.count(), "auteur(s)")
