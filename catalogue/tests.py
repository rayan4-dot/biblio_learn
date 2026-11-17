from django.test import TestCase, Client
from django.urls import reverse
from .models import Categorie, Ressource


class CatalogueTests(TestCase):
    fixtures = ["donnees_initiales.json"]

    def setUp(self):
        self.client = Client()

    def test_fixture_chargee(self):
        self.assertEqual(Categorie.objects.count(), 3)
        self.assertEqual(Ressource.objects.count(), 8)

    def test_page_liste(self):
        response = self.client.get(reverse("catalogue:liste"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python pour tous")

    def test_recherche(self):
        response = self.client.get(reverse("catalogue:liste") + "?q=python")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1 ressource(s) trouvée(s)")
        self.assertContains(response, "Python pour tous")

    def test_page_detail(self):
        response = self.client.get(reverse("catalogue:detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python pour tous")
        self.assertContains(response, "Nombre d'exemplaires")

    def test_page_detail_404(self):
        response = self.client.get(reverse("catalogue:detail", kwargs={"pk": 99}))
        self.assertEqual(response.status_code, 404)

    def test_page_categories(self):
        response = self.client.get(reverse("catalogue:categories"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Informatique")
        self.assertContains(response, "(3 ressources)")

    def test_page_par_categorie(self):
        response = self.client.get(reverse("catalogue:par_categorie", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Catalogue : Informatique")
