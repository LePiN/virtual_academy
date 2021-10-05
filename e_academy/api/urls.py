from django.urls import path

from .views import CourseAPIView
from .views import CoursesAPIView
from .views import EnrollmentAPIView
from .views import EnrollmentsAPIView
from .views import StudentAPIView
from .views import StudentsAPIView


urlpatterns = [
    path("courses/", CoursesAPIView.as_view(), name="courses"),
    path("courses/<int:pk>/", CourseAPIView.as_view(), name="course"),
    path("enrollments/", EnrollmentsAPIView.as_view(), name="enrollments"),
    path("enrollments/<int:pk>/", EnrollmentAPIView.as_view(), name="enrollment"),
    path("students/", StudentsAPIView.as_view(), name="students"),
    path("students/<int:pk>/", StudentAPIView.as_view(), name="student"),
]
