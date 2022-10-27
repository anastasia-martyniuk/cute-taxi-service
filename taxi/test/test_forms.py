from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, DriverSearchForm, CarSearchForm, \
    ManufacturerSearchForm


class ManufacturerFormTests(TestCase):
    def test_search_form_has_correct_placeholder(self):
        form = ManufacturerSearchForm()

        self.assertIn('placeholder="Search by name"', form.as_p())

class DriverFormTests(TestCase):
    @staticmethod
    def create_form(test_license_number):
        return DriverLicenseUpdateForm(
            data={"license_number": test_license_number}
        )

    def test_length_of_license_number_should_be_8(self):
        self.assertFalse(self.create_form("HEY123456789").is_valid())
        self.assertFalse(self.create_form("HEY123").is_valid())

    def test_first_3_characters_should_be_uppercase_letters(self):
        self.assertFalse(self.create_form("hey09876").is_valid())

    def test_last_5__should_be_digits(self):
        self.assertFalse(self.create_form("HEEEEY12345").is_valid())

    def test_valid_license_number(self):
        self.assertTrue(self.create_form("HEY12345").is_valid())

    def test_driver_creation_form_with_license_number_first_name_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user98765",
            "password2": "user98765",
            "first_name": "First test",
            "last_name": "Last test",
            "license_number": "ADD99999"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_search_form_has_correct_placeholder(self):
        form = DriverSearchForm()

        self.assertIn('placeholder="Search by username"', form.as_p())


class CarFormTests(TestCase):
    def test_search_form_has_correct_placeholder(self):
        form = CarSearchForm()

        self.assertIn('placeholder="Search by model"', form.as_p())
