import os
import importlib
from django.core.files.storage import FileSystemStorage


def get_storage_class(import_path):
    """Dynamically imports a storage class"""
    module_path, class_name = import_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

def get_class():
    if os.getenv("USE_AWS") == "True":
        return get_storage_class("storages.backends.s3boto3.S3Boto3Storage")()
    elif os.getenv("USE_GCS") == "True":
        return get_storage_class("storages.backends.gcloud.GoogleCloudStorage")()
    return FileSystemStorage()