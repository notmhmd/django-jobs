import os

# Set the DJANGO_ENV environment variable (development/production)
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    from .production import *
elif DJANGO_ENV == 'development':
    from .development import *
else:
    raise ValueError(f"Unknown DJANGO_ENV value: {DJANGO_ENV}")