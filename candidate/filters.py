import django_filters
from .models import Candidate, DEPARTMENT_CHOICES


class CandidateFilter(django_filters.FilterSet):
    department = django_filters.ChoiceFilter(choices=DEPARTMENT_CHOICES)

    class Meta:
        model = Candidate
        fields = ['department']