from datetime import timedelta

from django.test import TestCase

from e_campus.models import Course
from e_campus.models import Enrollment
from e_campus.models import Student
from api.serializers import CourseSerializer
from api.serializers import EnrollmentSerializer
from api.serializers import StudentSerializer


class TestCourseSerializer(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            description="Mock", duration=timedelta(hours=12), name="Foo"
        )
        self.course_serializer = CourseSerializer(self.course)
        self.course_expected_data = {
            "description": "Mock",
            "duration": "12:00:00",
            "name": "Foo",
        }

    def test_course_contains_expected_fields(self):
        courses_serialized = self.course_serializer.data

        self.assertEqual(
            set(courses_serialized.keys()),
            set(["description", "duration", "holder_image", "name"]),
        )

    def test_course_field_content(self):
        data = self.course_serializer.data

        for key in self.course_expected_data.keys():
            with self.subTest(key=key):
                self.assertEqual(data[key], self.course_expected_data[key])


class TestEnrollmentSerializer(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            description="Mock", duration=timedelta(hours=12), name="Foo"
        )
        self.student = Student.objects.create(
            name="Mock Silva", nickname="MS", phone="47999999999"
        )
        self.enroll = Enrollment.objects.create(
            course=self.course,
            date_close="2021-12-14",
            score=6,
            status="RE",
            student=self.student,
        )

        self.enroll_serializer = EnrollmentSerializer(self.enroll)
        self.enroll_expected_data = {
            "course": self.course.pk,
            "date_close": "2021-12-14",
            "score": "6.0",
            "status": "RE",
            "student": self.student.pk,
        }

    def test_enroll_contains_expected_fields(self):
        data = self.enroll_serializer.data

        self.assertEqual(
            set(data.keys()),
            set(["course", "date_close", "date_enroll", "score", "status", "student"]),
        )

    def test_enroll_field_content(self):
        data = self.enroll_serializer.data

        for key in self.enroll_expected_data.keys():
            with self.subTest(key=key):
                self.assertEqual(data[key], self.enroll_expected_data[key])


class TestStudentSerializer(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="Mock Silva", nickname="MS", phone="47999999999"
        )
        self.student_serializer = StudentSerializer(self.student)
        self.student_expected_data = {
            "name": "Mock Silva",
            "nickname": "MS",
            "phone": "47999999999",
        }

    def test_student_contains_expected_fields(self):
        data = self.student_serializer.data

        self.assertEqual(set(data.keys()), set(["avatar", "name", "nickname", "phone"]))

    def test_student_field_content(self):
        data = self.student_serializer.data

        for key in self.student_expected_data.keys():
            with self.subTest(key=key):
                self.assertEqual(data[key], self.student_expected_data[key])
