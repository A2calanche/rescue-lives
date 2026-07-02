from django.core.exceptions import ValidationError
from django.test import TestCase

from rescue.models import AffectedPerson, LocationReport
from rescue.services import create_person_report


class AffectedPersonValidationTests(TestCase):
    def test_deceased_person_cannot_have_reference_photo(self):
        person = AffectedPerson(
            first_name="Ana",
            last_name="Pérez",
            current_status="DECEASED",
            reference_photo_url="https://example.com/photo.jpg",
        )

        with self.assertRaises(ValidationError):
            person.full_clean()

    def test_create_person_report_saves_location_and_person(self):
        payload = {
            "first_name": "Luis",
            "last_name": "Mendoza",
            "current_status": "MISSING",
            "reference_photo_url": "https://example.com/missing.jpg",
            "latitude": 10.4806,
            "longitude": -66.9036,
            "address_description": "Centro de acopio",
        }

        person, location = create_person_report(payload)

        self.assertIsInstance(person, AffectedPerson)
        self.assertIsInstance(location, LocationReport)
        self.assertEqual(person.current_status, "MISSING")
        self.assertEqual(location.person, person)
