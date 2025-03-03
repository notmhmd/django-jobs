#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoJobs.settings')
    # Set environment-specific settings based on DJANGO_ENV
    if os.getenv('DJANGO_ENV') == 'production':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoJobs.settings.production'
    elif os.getenv('DJANGO_ENV') == 'development':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoJobs.settings.development'
    elif os.getenv('DJANGO_ENV') == 'testing':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoJobs.settings.test'
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
