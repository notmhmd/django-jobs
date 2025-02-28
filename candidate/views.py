import os

import magic
import requests
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from common.auth import IsAdminPermission, KeycloakAuthentication
from common.paginations import CustomPagination
from .filters import CandidateFilter
from .models import Candidate
from .serializers import CandidateSerializer, CandidateListSerializer

ALLOWED_FILE_TYPES = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]


class CandidateRegisterView(generics.CreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        file = self.request.FILES.get("resume")

        # Validate File Type
        mime = magic.Magic(mime=True)
        file_mime = mime.from_buffer(file.read(2048))
        file.seek(0)

        if file_mime not in ALLOWED_FILE_TYPES:
            raise ValidationError({"error": "Invalid file type."}, code=status.HTTP_400_BAD_REQUEST)

        # Validate File Size (Max: 5MB)
        if file.size > 5 * 1024 * 1024:
            raise ValidationError({"error": "File too large. Max 5MB allowed."}, code=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        from .tasks import register_candidate_task
        serializer.validated_data.pop("resume", None)
        register_candidate_task.delay(serializer.validated_data)


# List Candidates (Admin Only)
class CandidateListView(generics.ListAPIView):
    queryset = Candidate.objects.all().order_by('-created')
    serializer_class = CandidateListSerializer
    authentication_classes = (KeycloakAuthentication,)
    permission_classes = [IsAdminPermission]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidateFilter




# Resume Download (Admin Only)
class ResumeDownloadView(generics.RetrieveAPIView):
    authentication_classes = (KeycloakAuthentication,)
    permission_classes = [IsAdminPermission]
    queryset = None

    def get(self, request, pk):
        candidate = get_object_or_404(Candidate, pk=pk)
        os.environ.setdefault("USE_AWS", "True")

        if not candidate.resume:
            return Response({"error": "Resume not found"}, status=404)

        file_path = candidate.resume.name
        try:
            file = default_storage.open(file_path, 'rb')
            return FileResponse(file, as_attachment=True, filename=candidate.resume.name.split("/")[-1])
        except FileNotFoundError:
            return Response({"error": "File not found"}, status=404)


class KeycloakLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        keycloak_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
        payload = {"client_id": settings.KEYCLOAK_CLIENT_ID, "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
            "grant_type": "password", "username": username, "password": password, "scope": "openid", }

        response = requests.post(keycloak_url, data=payload)
        print(response.json())

        if response.status_code != 200:
            return Response({"error": "Invalid credentials"}, status=response.status_code)

        return Response(response.json(), status=status.HTTP_200_OK)
