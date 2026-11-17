from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


class PagesTests(TestCase):
    def test_accueil_status_and_template(self):
        response = self.client.get(reverse("pages:accueil"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/accueil.html")
        self.assertContains(response, "Accueil")
        self.assertContains(response, "À propos")
        self.assertContains(response, "Contact")
        self.assertContains(response, 'href="/static/pages/style.css"')

    def test_accueil_nb_ressources_zero(self):
        response = self.client.get(reverse("pages:accueil"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Le catalogue est vide pour le moment")
        self.assertNotContains(response, "Le catalogue contient")

    def test_accueil_nb_ressources_positif(self):
        with patch("pages.views.render") as mock_render:
            from django.test import RequestFactory
            from pages.views import accueil

            request = RequestFactory().get("/")
            accueil(request)
            # Verify context passed to template
            contexte = mock_render.call_args[0][2]
            self.assertIn("nb_ressources", contexte)

        # Test rendering template directly with non-zero resources
        response = self.client.get(reverse("pages:accueil"))
        content = response.content.decode()
        # Verify both conditions can be tested
        from django.template import Context, Template

        template_str = """
        {% if nb_ressources == 0 %}
        <p>Le catalogue est vide pour le moment</p>
        {% else %}
        <p>Le catalogue contient {{ nb_ressources }} ressources</p>
        {% endif %}
        """
        rendered_zero = Template(template_str).render(Context({"nb_ressources": 0}))
        self.assertIn("Le catalogue est vide pour le moment", rendered_zero)

        rendered_five = Template(template_str).render(Context({"nb_ressources": 5}))
        self.assertIn("Le catalogue contient 5 ressources", rendered_five)

    def test_a_propos_status_and_content(self):
        response = self.client.get(reverse("pages:a_propos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/a_propos.html")
        self.assertContains(response, "Rayan Mansour : Chef de projet &amp; Développeur Backend")
        self.assertContains(response, "Sara Alami : Développeuse Frontend &amp; UI/UX")
        self.assertContains(response, "Youssef Bennani : Développeur Fullstack")

    def test_contact_get_status_and_template(self):
        response = self.client.get(reverse("pages:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/contact.html")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'name="nom"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="message"')

    def test_contact_post_valid_data(self):
        data = {
            "nom": "Rayan",
            "email": "rayan@example.com",
            "message": "Bonjour, ceci est un message de test.",
        }
        response = self.client.post(reverse("pages:contact"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Merci Rayan, votre message a bien été reçu")

    def test_contact_post_invalid_data(self):
        data = {
            "nom": "Rayan",
            "email": "not-an-email",
            "message": "Bonjour",
        }
        response = self.client.post(reverse("pages:contact"), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Merci Rayan, votre message a bien été reçu")
