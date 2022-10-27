from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver12345",
            license_number="AAA12345"
        )

    def test_driver_license_number_listed(self):
        """Tests than driver's license number is in list_display on driver admin page"""
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_detailed_license_number_listed(self):
        """Tests than driver's license number is on driver detail admin page"""
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        res = self.client.get(url)

        self.assertContains(res, self.driver.license_number)

    def test_driver_create_first_name_and_last_name_listed(self):
        """Tests than fields first name and last name are on driver create admin page"""
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)

        self.assertContains(res, self.driver.first_name)
        self.assertContains(res, self.driver.last_name)
