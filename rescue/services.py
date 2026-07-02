from .models import AffectedPerson, LocationReport


def create_person_report(data):
    person = AffectedPerson.objects.create(
        first_name=data["first_name"],
        last_name=data["last_name"],
        document_id=data.get("document_id"),
        age=data.get("age"),
        current_status=data.get("current_status", "MISSING"),
        medical_conditions=data.get("medical_conditions"),
        reference_photo_url=data.get("reference_photo_url"),
    )
    location = LocationReport.objects.create(
        person=person,
        latitude=data["latitude"],
        longitude=data["longitude"],
        address_description=data.get("address_description", ""),
        is_verified=data.get("is_verified", False),
    )
    return person, location
