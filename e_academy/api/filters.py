from django_filters import FilterSet
from django_filters.rest_framework import filters

from e_campus.models import Enrollment
from e_campus.models import Student


class EnrollmentsFilter(FilterSet):
    date_enroll_start = filters.DateFilter(field_name="date_enroll", lookup_expr="gte")
    date_enroll_end = filters.DateFilter(field_name="date_enroll", lookup_expr="lte")
    date_close_start = filters.DateFilter(field_name="date_close", lookup_expr="gte")
    date_close_end = filters.DateFilter(field_name="date_close", lookup_expr="lte")

    class Meta:
        model = Enrollment
        fields = [
            "course",
            "date_close_end",
            "date_close_start",
            "date_enroll_end",
            "date_enroll_start",
            "status",
            "student",
        ]


class StudentsFilter(FilterSet):
    date_created_start = filters.DateFilter(
        field_name="date_created", lookup_expr="gte"
    )
    date_created_end = filters.DateFilter(field_name="date_created", lookup_expr="lte")

    class Meta:
        model = Student
        fields = ["date_created_end", "date_created_start"]
