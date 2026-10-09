from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "user",
            "job",
            "status",
            "applied_at",
            "resume_version",
            "notes",
            "created_at",
            "updated_at",
        ]
        
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]