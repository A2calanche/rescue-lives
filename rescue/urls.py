from django.urls import path

from .views import create_report, health_check, nearby_locations

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("reports/", create_report, name="create-report"),
    path("locations/nearby/", nearby_locations, name="nearby-locations"),
]
