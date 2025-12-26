from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Equipment, EquipmentType, Site, Workshop


class EquipmentModelTests(TestCase):
    def setUp(self) -> None:
        self.site_a = Site.objects.create(name="Площадка А")
        self.site_b = Site.objects.create(name="Площадка Б")
        self.workshop_a1 = Workshop.objects.create(site=self.site_a, name="Цех 1")
        self.eq_type = EquipmentType.objects.create(name="Насос")

    def test_workshop_must_match_site(self):
        equipment = Equipment(
            name="Тестовое оборудование",
            inventory_number="INV-1",
            equipment_type=self.eq_type,
            site=self.site_b,
            workshop=self.workshop_a1,
        )
        with self.assertRaises(ValidationError):
            equipment.clean()


class CatalogViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.site = Site.objects.create(name="Основная")
        self.workshop = Workshop.objects.create(site=self.site, name="Цех 1")
        self.eq_type = EquipmentType.objects.create(name="Станок")
        self.equipment = Equipment.objects.create(
            name="Станок 1",
            inventory_number="INV-100",
            equipment_type=self.eq_type,
            site=self.site,
            workshop=self.workshop,
        )
        user_model = get_user_model()
        self.user = user_model.objects.create_user("tester", password="password123")

    def test_equipment_list_available(self):
        response = self.client.get(reverse("catalog:equipment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.equipment.name)

    def test_add_to_cart_requires_auth(self):
        response = self.client.post(
            reverse("catalog:add_to_cart", args=[self.equipment.pk]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(reverse("accounts:login"), response.redirect_chain[0][0])

        self.client.login(username="tester", password="password123")
        response = self.client.post(
            reverse("catalog:add_to_cart", args=[self.equipment.pk]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корзина")
