from django.contrib import admin
from .models import Auteur, Categorie, Ressource


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom", "description")
    search_fields = ("nom",)


@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom")
    search_fields = ("nom", "prenom")


@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "type_ressource",
        "categorie",
        "afficher_auteurs",
        "annee",
        "nb_exemplaires",
        "disponible",
    )
    list_filter = ("type_ressource", "categorie", "disponible")
    search_fields = ("titre", "resume")
    list_editable = ("disponible",)
    filter_horizontal = ("auteurs",)

    @admin.display(description="Auteurs")
    def afficher_auteurs(self, obj):
        return ", ".join(str(a) for a in obj.auteurs.all())

admin.site.site_header = "🏛️ BiblioLearn Administration"
admin.site.site_title = "BiblioLearn Admin"
admin.site.index_title = "Supervision du Catalogue & des Ressources Académiques"
