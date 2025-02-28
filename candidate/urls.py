from django.urls import path
from .views import CandidateRegisterView, CandidateListView, ResumeDownloadView, KeycloakLoginView

urlpatterns = [
    path("register/", CandidateRegisterView.as_view(), name="candidate-register"),
    path("login/", KeycloakLoginView.as_view(), name="keycloak-candidate-login"),
    path("admin/candidates/", CandidateListView.as_view(), name="candidate-list"),
    path("admin/candidate/<int:pk>/resume/", ResumeDownloadView.as_view(), name="resume-download"),
]