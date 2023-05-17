from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Data, Project


class DataTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(
            name="Test Project", description="Test project description", owner=self.user
        )
        self.data = Data.objects.create(
            name="Test Data", description="Test data description", project=self.project
        )

    def test_data_list(self):
        response = self.client.get(reverse("core:data_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "data_list.html")

    def test_data_detail(self):
        response = self.client.get(reverse("core:data_detail", args=[self.data.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "data_detail.html")

    def test_data_create(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("core:data_create"),
            {
                "name": "New Data",
                "description": "New data description",
                "project_id": self.project.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Data.objects.count(), 2)

    def test_data_update(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("core:data_update", args=[self.data.id]),
            {
                "name": "Updated Data",
                "description": "Updated data description",
                "project_id": self.project.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.data.refresh_from_db()
        self.assertEqual(self.data.name, "Updated Data")

    def test_data_delete(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("core:data_delete", args=[self.data.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Data.objects.count(), 0)
