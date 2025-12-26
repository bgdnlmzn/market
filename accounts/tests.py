from django.test import Client, TestCase
from django.urls import reverse


class AuthViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_signup_page_renders(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Регистрация")

    def test_login_page_renders(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Вход")
