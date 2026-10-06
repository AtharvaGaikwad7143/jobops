from django.db import models
from django.conf import settings

from jobs.models import Job


class Application(models.Model):

    class Status(models.TextChoices):
        SAVED = "SAVED", "Saved"
        APPLIED = "APPLIED", "Applied"
        SCREENING = "SCREENING", "Screening"
        INTERVIEW = "INTERVIEW", "Interview"
        OFFER = "OFFER", "Offer"
        REJECTED = "REJECTED", "Rejected"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    status = models.CharField(
          max_length=20,
        choices=Status.choices,
        default=Status.SAVED,
    )

    applied_at = models.DateTimeField(null=True, blank=True)
    resume_version = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.job}"