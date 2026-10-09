from rest_framework import serializers

from .models import Company, Job


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "website"]


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "location",
            "description",
            "source",
            "source_url",
            "company",
            "discovered_at",
        ]
        read_only_fields = ["id", "discovered_at"]