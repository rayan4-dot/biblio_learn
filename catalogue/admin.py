from django.contrib import admin
from .models import Categorie, Ressource


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom", "description")
    search_fields = ("nom",)


@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ("titre", "type_ressource", "categorie", "annee", "nb_exemplaires", "disponible")
    list_filter = ("type_ressource", "categorie", "disponible")
    search_fields = ("titre", "resume")
    list_editable = ("disponible",)
