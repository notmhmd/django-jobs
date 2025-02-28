import os
import uuid
from datetime import datetime

from django.db import models
from model_utils.models import TimeStampedModel

from common.storage_backends import get_class

DEPARTMENT_CHOICES = [
    ("IT", "IT"),
    ("HR", "HR"),
    ("Finance", "Finance"),
]

def resume_upload_path(instance, filename):
    if instance.id is None:
        temp_filename = f"{uuid.uuid4()}.{filename.split('.')[-1]}"
        return os.path.join("resumes", "temp", temp_filename)  # Temporary location
    else:
        ext = filename.split('.')[-1]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{instance.id}_{timestamp}_{uuid.uuid4()}.{ext}"
        return os.path.join("resumes", str(instance.id), unique_filename)


class Candidate(TimeStampedModel):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    years_of_experience = models.PositiveIntegerField()
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    resume = models.FileField(upload_to=resume_upload_path, storage=get_class())
    auth_id = models.UUIDField(default=None, editable=False, null=True)
    email = models.EmailField(unique=True, default=None, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.resume and self.resume.name.startswith('resumes/temp/'):
            final_path = resume_upload_path(self, self.resume.name.split('/')[-1])
            storage = self.resume.storage
            storage.save(final_path, self.resume)
            storage.delete(self.resume.name)
            self.resume.name = final_path
            super().save(update_fields=['resume'])

    def __str__(self):
        return self.full_name