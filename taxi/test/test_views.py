from django.contrib.auth import get_user_model
from django.test import TestCase,RequestFactory
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.views import ManufacturerListView, CarListView, DriverListView

HOME_URL = reverse("taxi:index")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicTests(TestCase):
    def test_login_required(self):
        res_home = self.client.get(HOME_URL)
        res_drivers = self.client.get(DRIVERS_URL)
        res_cars = self.client.get(CARS_URL)
        res_manufacturers = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res_home.status_code, 200)
        self.assertNotEqual(res_drivers.status_code, 200)
        self.assertNotEqual(res_cars.status_code, 200)
        self.assertNotEqual(res_manufacturers.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1345"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Volkswagen", country="Germany")
        Manufacturer.objects.create(name="Ford", country="USA")

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer(self):
        request = self.factory.get("manufacturers/?name=test")
        request.user = self.user
        response = ManufacturerListView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user98765",
            "password2": "user98765",
            "first_name": "First test",
            "last_name": "Last test",
            "license_number": "ADD99999"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])




class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1345"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVERS_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver(self):
        request = self.factory.get("manufacturers/?username=test")
        request.user = self.user
        response = DriverListView.as_view()(request)

        self.assertEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password1345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        Car.objects.create(model="Test", manufacturer=Manufacturer.objects.create(name="Ford", country="USA"))

        response = self.client.get(CARS_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car(self):
        request = self.factory.get("manufacturers/?model=test")
        request.user = self.user
        response = CarListView.as_view()(request)

        self.assertEqual(response.status_code, 200)
