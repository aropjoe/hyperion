from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Project


class ProjectTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(
            name="Test Project", description="Test project description", owner=self.user
        )

    def test_project_list(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("core:project_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_list.html")

    def test_project_detail(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("core:project_detail", args=[self.project.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_detail.html")

    def test_project_create(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("core:project_create"),
            {"name": "New Project", "description": "New project description"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 2)

    def test_project_update(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("core:project_update", args=[self.project.id]),
            {"name": "Updated Project", "description": "Updated project description"},
        )
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Project")

    def test_project_delete(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("core:project_delete", args=[self.project.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Project.objects.count(), 0)
