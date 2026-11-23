from django.urls import path
from . import views

app_name = "catalogue"

urlpatterns = [
    path("", views.liste, name="liste"),
    path("categories/", views.categories, name="categories"),
    path("categorie/<int:pk>/", views.par_categorie, name="par_categorie"),
    path("auteur/<int:pk>/", views.par_auteur, name="par_auteur"),
    path("<int:pk>/", views.detail, name="detail"),
]
