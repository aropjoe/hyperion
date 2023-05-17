from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_projects"
    )
    collaborators = models.ManyToManyField(User, related_name="collaborating_projects")

    def data_list(self):
        return Data.objects.filter(project=self)

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(upload_to="files/")
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.PositiveIntegerField(default=0)
    file_mime_type = models.CharField(max_length=100, default="Unknown")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set the file metadata before saving
        self.file_name = self.file.name
        self.file_size = self.file.size
        self.file_mime_type = self.file.file.content_type

        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name


class Data(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_data", blank=True, null=True
    )
    files = models.ManyToManyField(File, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_updated"]

    def __str__(self):
        return self.name


class Analysis(models.Model):
    title = models.CharField(max_length=255)
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    insights = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name="collaborating_analyses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
