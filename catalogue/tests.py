from django.test import TestCase, Client
from django.urls import reverse
from .models import Auteur, Categorie, Ressource


class CatalogueTests(TestCase):
    fixtures = ["donnees_initiales.json", "auteurs.json"]

    def setUp(self):
        self.client = Client()
        # Liaison des auteurs pour les tests
        a_amrani = Auteur.objects.get(nom="Amrani")
        a_benali = Auteur.objects.get(nom="Benali")
        a_idrissi = Auteur.objects.get(nom="El Idrissi")
        a_tazi = Auteur.objects.get(nom="Tazi")
        a_chraibi = Auteur.objects.get(nom="Chraibi")

        Ressource.objects.get(titre="Python pour tous").auteurs.set([a_amrani])
        Ressource.objects.get(titre="Apprendre Django pas à pas").auteurs.set([a_amrani, a_benali])
        Ressource.objects.get(titre="Introduction aux bases de données").auteurs.set([a_benali])
        Ressource.objects.get(titre="Algèbre linéaire").auteurs.set([a_idrissi])
        Ressource.objects.get(titre="Probabilités et statistiques").auteurs.set([a_idrissi, a_tazi])
        Ressource.objects.get(titre="Les graphes en pratique").auteurs.set([a_tazi])
        Ressource.objects.get(titre="Grammaire française").auteurs.set([a_chraibi])
        Ressource.objects.get(titre="Histoire de la littérature arabe").auteurs.set([a_chraibi])

    def test_fixtures_chargees(self):
        self.assertEqual(Categorie.objects.count(), 3)
        self.assertEqual(Ressource.objects.count(), 8)
        self.assertEqual(Auteur.objects.count(), 5)

    def test_page_liste_et_pagination(self):
        response = self.client.get(reverse("catalogue:liste"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "8 ressource(s) trouvée(s)")
        self.assertContains(response, "Page 1 sur 3")

    def test_recherche_titre_et_auteur(self):
        response = self.client.get(reverse("catalogue:liste") + "?q=tazi")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2 ressource(s) trouvée(s)")
        self.assertContains(response, "Les graphes en pratique")
        self.assertContains(response, "Probabilités et statistiques")

    def test_tri_recent(self):
        response = self.client.get(reverse("catalogue:liste") + "?tri=recent")
        self.assertEqual(response.status_code, 200)
        # 2024 doit être en premier
        self.assertContains(response, "Les graphes en pratique")

    def test_page_detail(self):
        response = self.client.get(reverse("catalogue:detail", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apprendre Django pas à pas")
        self.assertContains(response, "Salma Amrani")
        self.assertContains(response, "Karim Benali")

    def test_page_detail_404(self):
        response = self.client.get(reverse("catalogue:detail", kwargs={"pk": 99}))
        self.assertEqual(response.status_code, 404)

    def test_page_auteurs(self):
        response = self.client.get(reverse("catalogue:auteurs"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Salma Amrani")
        self.assertContains(response, "(2 ressources)")

    def test_page_par_auteur(self):
        response = self.client.get(reverse("catalogue:par_auteur", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apprendre Django pas à pas")
        self.assertContains(response, "Python pour tous")
