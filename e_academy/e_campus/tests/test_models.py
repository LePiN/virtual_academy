from datetime import timedelta

from django.test import TestCase

from e_campus.models import Course
from e_campus.models import Enrollment
from e_campus.models import Student


class TestCourse(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            description="Mock", duration=timedelta(hours=12), name="Foo"
        )
        self.course_str = "Foo"

    def test_course_creation(self):
        self.assertIsInstance(self.course, Course)
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(self.course.__str__(), self.course_str)


class TestEnrollment(TestCase):
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
        self.enroll_str = "Mock Silva/Foo/RE"

    def test_enroll_creation(self):
        self.assertIsInstance(self.enroll, Enrollment)
        self.assertEqual(Enrollment.objects.all().count(), 1)
        self.assertEqual(self.enroll.__str__(), self.enroll_str)


class TestStudent(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="Mock Silva", nickname="MS", phone="47999999999"
        )
        self.student_str = "Mock Silva"

    def test_student_creation(self):
        self.assertIsInstance(self.student, Student)
        self.assertEqual(Student.objects.all().count(), 1)
        self.assertEqual(self.student.__str__(), self.student_str)
