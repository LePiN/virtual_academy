from rest_framework import serializers

from e_campus.models import Course
from e_campus.models import Student
from e_campus.models import Enrollment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("description", "duration", "holder_image", "name")


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            "avatar",
            "name",
            "nickname",
            "phone",
        )


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = (
            "course",
            "date_close",
            "date_enroll",
            "score",
            "status",
            "student",
        )
