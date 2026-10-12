from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from applications.models import Application
from jobs.models import Company, Job


User = get_user_model()


class ApplicationIsolationTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username="alice",
            password="TestPass123!",
        )
        self.bob = User.objects.create_user(
            username="bob",
            password="TestPass123!",
        )

        self.company = Company.objects.create(
            name="Acme",
            website="https://example.com",
        )

        self.job = Job.objects.create(
            title="Backend Engineer",
            location="Pune",
            description="Build backend systems",
            source="linkedin",
            source_url="https://example.com/jobs/123",
            company=self.company,
        )

        self.alice_application = Application.objects.create(
            user=self.alice,
            job=self.job,
        )

        self.list_url = "/api/applications/"

    def test_user_cannot_see_another_users_application(self):
        self.client.force_authenticate(user=self.bob)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if isinstance(response.data, dict):
            items = response.data["results"]
        else:
            items = response.data

        visible_ids = [item["id"] for item in items]

        self.assertNotIn(
            self.alice_application.pk,
            visible_ids,
        )

    def test_user_cannot_retrieve_another_users_application(self):
        self.client.force_authenticate(user=self.bob)

        response = self.client.get(
            f"{self.list_url}{self.alice_application.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_client_cannot_assign_another_user_as_owner(self):
        self.client.force_authenticate(user=self.bob)

        response = self.client.post(
            self.list_url,
            {
                "user": self.alice.pk,
                "job": self.job.pk,
                "status": "SAVED",
                "notes": "Ownership security test",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        created_application = Application.objects.get(
            pk=response.data["id"]
        )

        self.assertEqual(created_application.user, self.bob)
        self.assertNotEqual(created_application.user, self.alice)


    def test_applications_are_paginated(self):
        self.client.force_authenticate(user=self.alice)

        for i in range(25):
            Application.objects.create(
                user=self.alice,
                job=self.job,
                status=Application.Status.SAVED,
            )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 20)


    def test_user_can_filter_applications_by_status(self):
        self.client.force_authenticate(user=self.alice)

        Application.objects.create(
            user=self.alice,
            job=self.job,
            status=Application.Status.SAVED,
        )

        Application.objects.create(
            user=self.alice,
            job=self.job,
            status=Application.Status.INTERVIEW,
        )

        Application.objects.create(
            user=self.alice,
            job=self.job,
            status=Application.Status.REJECTED,
        )

        response = self.client.get(
            self.list_url,
            {"status": Application.Status.INTERVIEW},
        )

        self.assertEqual(response.status_code, 200)

        results = response.data["results"]

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["status"],
            Application.Status.INTERVIEW,
        )


    def test_unauthenticated_user_cannot_access_applications(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 401)