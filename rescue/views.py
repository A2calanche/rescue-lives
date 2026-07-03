import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import AffectedPerson, LocationReport
from .services import create_person_report


@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({"status": "ok", "app": "rescue"})


@csrf_exempt
@require_http_methods(["POST"])
def create_report(request):
    payload = request.POST or json.loads(request.body or "{}")
    if not payload:
        return JsonResponse({"error": "Payload vacío"}, status=400)

    try:
        person, location = create_person_report(payload)
    except Exception as exc:  # pragma: no cover - simple API guard
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse(
        {
            "person_id": str(person.id),
            "status": person.current_status,
            "location_id": str(location.id),
        },
        status=201,
    )


@require_http_methods(["GET"])
def nearby_locations(request):
    qs = LocationReport.objects.select_related("person")
    data = [
        {
            "person_id": str(item.person.id),
            "full_name": f"{item.person.first_name} {item.person.last_name}",
            "status": item.person.current_status,
            "latitude": str(item.latitude),
            "longitude": str(item.longitude),
        }
        for item in qs[:20]
    ]
    return JsonResponse(data, safe=False)
