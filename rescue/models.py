import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class AffectedPerson(models.Model):
    STATUS_CHOICES = [
        ("MISSING", "Desaparecido"),
        ("FOUND", "Encontrado Vivo"),
        ("RESCUED", "Rescatado"),
        ("EVACUATED", "Evacuado en Refugio"),
        ("DECEASED", "Fallecido"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    document_id = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="MISSING")
    medical_conditions = models.TextField(blank=True, null=True)
    reference_photo_url = models.URLField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        super().clean()
        if self.current_status == "DECEASED" and self.reference_photo_url:
            raise ValidationError(
                {
                    "reference_photo_url": _(
                        "No se permiten fotos de referencia para personas fallecidas."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class LocationReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(AffectedPerson, on_delete=models.CASCADE, related_name="locations")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address_description = models.TextField(blank=True, default="")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Ubicación de {self.person}"
