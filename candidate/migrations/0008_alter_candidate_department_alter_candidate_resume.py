# Generated by Django 5.1.6 on 2025-03-03 17:35

import candidate.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0007_alter_candidate_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='department',
            field=models.CharField(choices=[('IT', 'IT'), ('HR', 'HR'), ('Finance', 'Finance')], db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='resume',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=candidate.models.resume_upload_path),
        ),
    ]
