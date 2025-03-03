from datetime import date
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from candidate.models import Candidate


class CandidateModelTest(TestCase):

    def setUp(self):
        self.candidate = Candidate.objects.create(
            full_name="John Test Doe",
            date_of_birth=date(1990, 5, 15),
            years_of_experience=5,
            department="IT",
            email="johndoe@example.com",
        )

    def test_candidate_creation(self):
        self.assertEqual(self.candidate.full_name, "John Test Doe")
        self.assertEqual(self.candidate.years_of_experience, 5)
        self.assertEqual(self.candidate.department, "IT")

    def test_candidate_resume_upload(self):
        resume_file = SimpleUploadedFile("resume.pdf", b"Dummy resume content")
        self.candidate.resume = resume_file
        self.candidate.save()
        self.assertTrue(self.candidate.resume.name.startswith("resumes/"))


class CandidateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = {"username": "johndoe", "resource_access": {"realm-management": {"roles": ["view-users"]}}}
        self.candidate = Candidate.objects.create(
            full_name="Jane Testing Doe",
            date_of_birth="1992-08-10",
            years_of_experience=3,
            department="HR",
            email="janedoe@example.com",
            resume=SimpleUploadedFile("resume.pdf", b"Dummy resume content"),
        )

        self.candidate_no_resume = Candidate.objects.create(
            full_name="John No Resume Doe",
            date_of_birth="1992-08-10",
            years_of_experience=3,
            department="HR",
            email="johndoe1@example.com",
        )

    def test_list_candidates(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("candidate-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json().get("results"), list)

    @patch('candidate.views.magic.Magic')
    @patch('candidate.tasks.register_candidate_task.delay')  # Mock the Celery task
    def test_create_candidate_valid(self, mock_register_candidate_task, MockMagic):
        MockMagic.return_value.from_buffer.return_value = "application/pdf"
        url = reverse("candidate-register")
        data = {
            "full_name": "John Doe",
            "date_of_birth": "1990-05-15",
            "years_of_experience": 5,
            "department": "IT",
            "email": "johndoe6@example.com",
            "resume": SimpleUploadedFile("resume.pdf", b"Dummy resume content", content_type="application/pdf"),
        }
        response = self.client.post(url, data, format="multipart")

        mock_register_candidate_task.assert_called()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "johndoe6@example.com")

    @patch('candidate.views.magic.Magic')
    def test_create_candidate_invalid_file_type(self, MockMagic):
        url = reverse("candidate-register")
        MockMagic.return_value.from_buffer.return_value = "text/plain"

        data = {
            "full_name": "Jane Doe",
            "date_of_birth": "1988-07-22",
            "years_of_experience": 3,
            "department": "HR",
            "email": "janedoe@example1.com",
            "resume": SimpleUploadedFile("resume.txt", b"Dummy resume content", content_type="text/plain"),
        }

        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid file type.")

    @patch('candidate.views.magic.Magic')
    def test_create_candidate_file_too_large(self, MockMagic):
        MockMagic.return_value.from_buffer.return_value = "application/pdf"

        url = reverse("candidate-register")
        large_file_content = b"A" * (6 * 1024 * 1024)  # 6MB file
        data = {
            "full_name": "Mark Smith",
            "date_of_birth": "1985-02-25",
            "years_of_experience": 7,
            "department": "IT",
            "email": "marksmitfh@example.com",
            "resume": SimpleUploadedFile("large_resume.pdf", large_file_content, content_type="application/pdf"),
        }

        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "File too large. Max 5MB allowed.")

    def test_create_candidate_missing_resume(self):
        url = reverse("candidate-register")

        data = {
            "full_name": "Sarah Lee",
            "date_of_birth": "1992-10-30",
            "years_of_experience": 4,
            "department": "Finance",
            "email": "sarahlee@example.com",
        }

        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("resume", response.data)

    def test_resume_download_view(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("resume-download", kwargs={"pk": self.candidate.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url_no_resume = reverse("resume-download", kwargs={"pk": self.candidate_no_resume.id})
        response_no_resume = self.client.get(url_no_resume)
        self.assertEqual(response_no_resume.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_token(self):
        self.client.defaults["HTTP_AUTHORIZATION"] = "Bearer invalidtoken"
        url = reverse("candidate-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_token(self):
        url = reverse("candidate-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
