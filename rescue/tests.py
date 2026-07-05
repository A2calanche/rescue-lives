from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

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

class HealthCheckTests(TestCase):
    def test_health_check_returns_ok(self):
        response = self.client.get("/api/v1/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

@override_settings(RESCUE_API_KEY="test-key-123")
class CreateReportTests(TestCase):
    def test_create_report_valid_payload_returns_201(self):
        payload = {
            "first_name": "Luis",
            "last_name": "Mendoza",
            "latitude": 10.48,
            "longitude": -66.90,
        }
        response = self.client.post(
            "/api/v1/reports/",
            data=payload,
            content_type="application/json",
            HTTP_X_API_KEY="test-key-123",
        )
        self.assertEqual(response.status_code, 201)

    def test_create_report_empty_payload_returns_400(self):
        response = self.client.post(
            "/api/v1/reports/",
            data={},
            content_type="application/json",
            HTTP_X_API_KEY="test-key-123",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_report_deceased_with_photo_fails(self):
        payload = {
            "first_name": "Ana",
            "last_name": "Pérez",
            "current_status": "DECEASED",
            "reference_photo_url": "https://example.com/photo.jpg",
            "latitude": 10.48,
            "longitude": -66.90,
        }
        response = self.client.post(
            "/api/v1/reports/",
            data=payload,
            content_type="application/json",
            HTTP_X_API_KEY="test-key-123",
        )
        self.assertEqual(response.status_code, 400)

class NearbyLocationsTests(TestCase):
    def test_nearby_locations_empty_returns_empty_list(self):
        response = self.client.get("/api/v1/locations/nearby/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_nearby_locations_returns_created_person(self):
        create_person_report({
            "first_name": "Luis",
            "last_name": "Mendoza",
            "latitude": 10.4806,
            "longitude": -66.9036,
        })
        response = self.client.get("/api/v1/locations/nearby/")
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["full_name"], "Luis Mendoza")

from django.test import TestCase, override_settings

@override_settings(RESCUE_API_KEY="test-key-123")
class ApiKeyAuthTests(TestCase):
    def test_create_report_without_api_key_returns_401(self):
        payload = {"first_name": "Luis", "last_name": "Mendoza", "latitude": 10.48, "longitude": -66.90}
        response = self.client.post("/api/v1/reports/", data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_create_report_with_wrong_api_key_returns_401(self):
        payload = {"first_name": "Luis", "last_name": "Mendoza", "latitude": 10.48, "longitude": -66.90}
        response = self.client.post(
            "/api/v1/reports/", data=payload, content_type="application/json",
            HTTP_X_API_KEY="wrong-key",
        )
        self.assertEqual(response.status_code, 401)

    def test_create_report_with_correct_api_key_returns_201(self):
        payload = {"first_name": "Luis", "last_name": "Mendoza", "latitude": 10.48, "longitude": -66.90}
        response = self.client.post(
            "/api/v1/reports/", data=payload, content_type="application/json",
            HTTP_X_API_KEY="test-key-123",
        )
        self.assertEqual(response.status_code, 201)
