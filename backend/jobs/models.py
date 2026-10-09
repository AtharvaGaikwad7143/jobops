from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    source = models.CharField(max_length=100)
    source_url = models.URLField(unique=True)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
    )

    discovered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"