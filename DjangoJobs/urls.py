"""
URL configuration for DjangoJobs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

# Set up the API schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Candidate API",
        default_version='v1',
        description="API for managing candidates and resumes",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mhmdfrj.97@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()



urlpatterns = [
    # path("admin/", admin.site.urls),
    path("api/candidates/", include("candidate.urls")),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs') if settings.DJANGO_ENV == 'development' else None,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DJANGO_ENV == 'development':
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),  # Correct URL pattern
    ]