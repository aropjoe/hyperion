# Generated by Django 4.1.7 on 2023-05-16 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0002_analysis_data_project_delete_dataset_data_project_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="data",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owned_data",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]