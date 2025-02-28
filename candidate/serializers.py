from rest_framework import serializers
from .models import Candidate, DEPARTMENT_CHOICES


class CandidateSerializer(serializers.ModelSerializer):
    department = serializers.ChoiceField(
        choices=dict(DEPARTMENT_CHOICES),
        error_messages={
            "invalid_choice": f"Invalid department. Choose from {', '.join(dict(DEPARTMENT_CHOICES).keys())}.",
            "required": f"Department must be one of {', '.join(dict(DEPARTMENT_CHOICES).keys())}"
        }
    )

    class Meta:
        model = Candidate
        fields = '__all__'


class CandidateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "full_name", "date_of_birth", "years_of_experience", "department"]