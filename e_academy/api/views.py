from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from e_campus.models import Course
from e_campus.models import Enrollment
from e_campus.models import Student
from .filters import EnrollmentsFilter
from .filters import StudentsFilter
from .serializers import CourseSerializer
from .serializers import EnrollmentSerializer
from .serializers import StudentSerializer


class CoursesAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollmentsAPIView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EnrollmentsFilter


class EnrollmentAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class StudentsAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentsFilter


class StudentAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
