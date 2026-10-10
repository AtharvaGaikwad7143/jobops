from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Application.objects.filter(user=self.request.user).select_related("job", "job__company")
        )

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)