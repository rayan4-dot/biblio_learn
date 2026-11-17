from django.db import models


class Categorie(models.Model):
    nom = models.CharField("Nom", max_length=100, unique=True)
    description = models.TextField("Description", blank=True)

    class Meta:
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Ressource(models.Model):
    TYPE_CHOIX = [
        ("livre", "Livre"),
        ("article", "Article"),
        ("cours", "Support de cours"),
    ]

    titre = models.CharField("Titre", max_length=200)
    type_ressource = models.CharField(
        "Type", max_length=20, choices=TYPE_CHOIX, default="livre"
    )
    resume = models.TextField("Résumé", blank=True)
    annee = models.PositiveIntegerField("Année", null=True, blank=True)
    nb_exemplaires = models.PositiveIntegerField("Nombre d'exemplaires", default=1)
    disponible = models.BooleanField("Disponible", default=True)
    date_ajout = models.DateTimeField("Date d'ajout", auto_now_add=True)
    categorie = models.ForeignKey(
        Categorie,
        verbose_name="Catégorie",
        on_delete=models.PROTECT,
        related_name="ressources",
    )

    class Meta:
        verbose_name = "ressource"
        verbose_name_plural = "ressources"
        ordering = ["titre"]

    def __str__(self):
        return self.titre
