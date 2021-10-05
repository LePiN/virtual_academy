from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from e_campus.models import Course
from e_campus.models import Enrollment
from e_campus.models import Student
from .serializers import CourseSerializer
from .serializers import EnrollmentSerializer
from .serializers import StudentSerializer


def image_default():
    small_gif = (
        b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
        b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
        b"\x02\x4c\x01\x00\x3b"
    )
    return SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")


class TestCourseAPI(APITestCase):
    required_fields = ["description", "duration", "name"]
    invalid_course = {"duration": "xxx", "holder_image": "wrong.jpg"}

    def setUp(self):
        self.course_a = Course.objects.create(
            description="Mock 1", duration=timedelta(hours=12), name="Foo 1"
        )
        self.course_b = Course.objects.create(
            description="Mock 2", duration=timedelta(hours=24), name="Foo 2"
        )
        self.course_c = Course.objects.create(
            description="Mock 3", duration=timedelta(hours=36), name="Foo 3"
        )
        self.course_d = Course.objects.create(
            description="Mock 4", duration=timedelta(hours=48), name="Foo 4"
        )

    def test_get_all_courses(self):
        courses = Course.objects.all()
        courses_serialized = CourseSerializer(courses, many=True)

        response = self.client.get(reverse("courses"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data, courses_serialized.data)

    def test_get_valid_single_course(self):
        course = Course.objects.get(pk=self.course_c.pk)
        course_serialized = CourseSerializer(course)

        response = self.client.get(reverse("course", kwargs={"pk": self.course_c.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data, course_serialized.data)

    def test_get_nonexistent_single_course(self):
        response = self.client.get(reverse("course", kwargs={"pk": 99}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(response.data, dict)

    def test_post_create_valid_course(self):
        previous_number_courses = Course.objects.all().count()
        data = {
            "description": "Mock 5",
            "duration": 7200,
            "holder_image": "",
            "name": "Foo 5",
        }

        response = self.client.post(reverse("courses"), data)
        result = Course.objects.last()

        self.assertEqual(result, result)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), previous_number_courses + 1)
        self.assertEqual(data["description"], result.description)
        self.assertEqual(timedelta(seconds=data["duration"]), result.duration)
        self.assertEqual(data["name"], result.name)

    def test_post_create_invalid_course(self):
        previous_number_courses = Course.objects.all().count()
        data = {
            "description": "Mock 5",
            "duration": 7200,
            "holder_image": "",
            "name": "Foo 5",
        }

        for field in self.required_fields:
            with self.subTest(field=field):
                data.pop(field)
                response = self.client.post(reverse("courses"), data)
                result = Course.objects.last()

                self.assertEqual(result, result)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(Course.objects.all().count(), previous_number_courses)

    def test_put_update_valid_course(self):
        course = Course.objects.get(pk=self.course_d.pk)
        data = {
            "description": "New Mock",
            "duration": "03:00:00",
            "holder_image": image_default(),
            "name": "New Foo",
        }

        self.assertNotEqual(course.description, data["description"])
        self.assertNotEqual(course.duration, data["duration"])
        self.assertNotEqual(course.name, data["name"])

        response = self.client.put(
            reverse("course", kwargs={"pk": self.course_d.pk}), data=data
        )
        result = Course.objects.last()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.description, data["description"])
        self.assertEqual(result.duration, timedelta(seconds=10800))
        self.assertEqual(result.name, data["name"])

    def test_put_update_invalid_course(self):
        duration_error = [
            "Formato inválido para Duração. Use um dos formatos a seguir: [DD] [HH:[MM:]]ss[.uuuuuu]."
        ]
        image_error = [
            "O dado submetido não é um arquivo. Certifique-se do tipo de codificação no formulário."
        ]
        required_error = ["Este campo é obrigatório."]

        response = self.client.put(
            reverse("course", kwargs={"pk": self.course_d.pk}), data=self.invalid_course
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["description"], required_error)
        self.assertEqual(response.data["duration"], duration_error)
        self.assertEqual(response.data["holder_image"], image_error)
        self.assertEqual(response.data["name"], required_error)

    def test_put_update_nonexistent_course(self):
        data = {
            "description": "New Mock",
            "duration": "03:00:00",
            "holder_image": image_default(),
            "name": "New Foo",
        }

        response = self.client.put(reverse("course", kwargs={"pk": 99}), data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_update_valid_course(self):
        course = Course.objects.get(pk=self.course_d.pk)
        update_data = {
            "description": "New Mock",
            "duration": "03:00:00",
            "holder_image": image_default(),
            "name": "New Foo",
        }

        self.assertNotEqual(course.description, update_data["description"])
        self.assertNotEqual(course.duration, update_data["duration"])
        self.assertNotEqual(course.name, update_data["name"])

        for key, value in update_data.items():
            with self.subTest(key=key, value=value):
                data = {key: value}
                response = self.client.patch(
                    reverse("course", kwargs={"pk": self.course_d.pk}), data=data
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_update_invalid_course(self):
        for key, value in self.invalid_course.items():
            with self.subTest(key=key, value=value):
                data = {key: value}
                response = self.client.patch(
                    reverse("course", kwargs={"pk": self.course_d.pk}), data=data
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_update_nonexistent_course(self):
        for key, value in self.invalid_course.items():
            with self.subTest(key=key, value=value):
                data = {key: value}
                response = self.client.patch(
                    reverse("course", kwargs={"pk": 99}), data=data
                )

                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_course(self):
        previous_number_courses = Course.objects.all().count()

        response = self.client.delete(
            reverse("course", kwargs={"pk": self.course_d.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), previous_number_courses - 1)

    def test_delete_nonexistent_course(self):
        previous_number_courses = Course.objects.all().count()

        response = self.client.delete(reverse("course", kwargs={"pk": 99}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Course.objects.all().count(), previous_number_courses)


class TestEnrollmentAPI(APITestCase):
    required_fields = ["course", "status", "student"]
    invalid_enrollment = {
        "course": "z",
        "date_close": "xxx",
        "score": 1000,
        "status": "Foo",
        "student": "b",
    }

    def setUp(self):
        self.course_a = Course.objects.create(
            description="Mock 1", duration=timedelta(hours=12), name="Foo 1"
        )
        self.course_b = Course.objects.create(
            description="Mock 2", duration=timedelta(hours=24), name="Foo 2"
        )
        self.course_c = Course.objects.create(
            description="Mock 3", duration=timedelta(hours=36), name="Foo 3"
        )
        self.student_a = Student.objects.create(
            name="Mock Silva", nickname="MS", phone="47999999999"
        )
        self.student_b = Student.objects.create(
            name="Mock Faria", nickname="MF", phone="47888888888"
        )
        self.enroll_a = Enrollment.objects.create(
            course=self.course_a, score=9, status="AN", student=self.student_a
        )
        self.enroll_b = Enrollment.objects.create(
            course=self.course_b,
            date_close="2021-12-14",
            score=6,
            status="RE",
            student=self.student_b,
        )

    def test_get_all_enrollments(self):
        enrollments = Enrollment.objects.all()
        enrollments_serialized = EnrollmentSerializer(enrollments, many=True)

        response = self.client.get(reverse("enrollments"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, enrollments_serialized.data)

    def test_get_valid_single_enrollment(self):
        enroll = Enrollment.objects.get(pk=self.enroll_a.pk)
        enroll_serialized = EnrollmentSerializer(enroll)

        response = self.client.get(
            reverse("enrollment", kwargs={"pk": self.enroll_a.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data, enroll_serialized.data)

    def test_get_nonexistent_single_enrollment(self):
        response = self.client.get(reverse("enrollment", kwargs={"pk": 99}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(response.data, dict)

    def test_post_create_valid_enrollment(self):
        previous_number_courses = Enrollment.objects.all().count()
        data = {
            "course": self.course_a.pk,
            "date_close": "2022-06-15",
            "score": 3,
            "status": "AN",
            "student": self.student_b.pk,
        }

        response = self.client.post(reverse("enrollments"), data)
        result = Enrollment.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.all().count(), previous_number_courses + 1)
        self.assertEqual(data["course"], result.course.pk)
        self.assertEqual(data["date_close"], result.date_close.strftime("%Y-%m-%d"))
        self.assertEqual(data["score"], result.score)
        self.assertEqual(data["status"], result.status)
        self.assertEqual(data["student"], result.student.pk)

    def test_post_create_invalid_enrollment(self):
        previous_number_enrollments = Enrollment.objects.all().count()
        data = {
            "course": self.course_a.pk,
            "date_close": "2022-06-15",
            "score": 3,
            "status": "AN",
            "student": self.student_b.pk,
        }

        for field in self.required_fields:
            with self.subTest(field=field):
                data.pop(field)
                response = self.client.post(reverse("enrollments"), data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(
                    Enrollment.objects.all().count(), previous_number_enrollments
                )

    def test_put_update_valid_enrollment(self):
        enrollment = Enrollment.objects.get(pk=self.enroll_b.pk)
        data = {
            "course": self.course_c.pk,
            "date_close": "2022-06-15",
            "score": 3,
            "status": "AN",
            "student": self.student_a.pk,
        }

        self.assertNotEqual(enrollment.course.pk, data["course"])
        self.assertNotEqual(
            enrollment.date_close.strftime("%Y-%m-%d"), data["date_close"]
        )
        self.assertNotEqual(enrollment.score, data["score"])
        self.assertNotEqual(enrollment.status, data["status"])
        self.assertNotEqual(enrollment.student.pk, data["student"])

        response = self.client.put(
            reverse("enrollment", kwargs={"pk": self.enroll_b.pk}), data=data
        )
        result = Enrollment.objects.last()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.course.pk, data["course"])
        self.assertEqual(result.date_close.strftime("%Y-%m-%d"), data["date_close"])
        self.assertEqual(result.score, data["score"])
        self.assertEqual(result.status, data["status"])
        self.assertEqual(result.student.pk, data["student"])

    def test_put_update_invalid_enrollment(self):
        response = self.client.put(
            reverse("enrollment", kwargs={"pk": self.enroll_b.pk}),
            data=self.invalid_enrollment,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_update_nonexistent_enrollment(self):
        data = {
            "course": self.course_c.pk,
            "date_close": "2022-06-15",
            "score": 3,
            "status": "AN",
            "student": self.student_a.pk,
        }

        response = self.client.put(reverse("enrollment", kwargs={"pk": 99}), data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_update_valid_enrollment(self):
        enrollment = Enrollment.objects.get(pk=self.enroll_b.pk)
        update_data = {
            "course": self.course_c.pk,
            "date_close": "2022-06-15",
            "score": 3,
            "status": "AN",
            "student": self.student_a.pk,
        }

        self.assertNotEqual(enrollment.course.pk, update_data["course"])
        self.assertNotEqual(
            enrollment.date_close.strftime("%Y-%m-%d"), update_data["date_close"]
        )
        self.assertNotEqual(enrollment.score, update_data["score"])
        self.assertNotEqual(enrollment.status, update_data["status"])
        self.assertNotEqual(enrollment.student.pk, update_data["student"])

        for key, value in update_data.items():
            with self.subTest(key=key, value=value):
                data = {key: value}
                response = self.client.patch(
                    reverse("enrollment", kwargs={"pk": self.enroll_b.pk}), data=data
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_update_invalid_enrollment(self):
        for key, value in self.invalid_enrollment.items():
            with self.subTest(key=key, value=value):
                data = {key: value}
                response = self.client.patch(
                    reverse("enrollment", kwargs={"pk": self.enroll_b.pk}), data=data
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_update_nonexistent_enrollment(self):
        for key, value in self.invalid_enrollment.items():
            with self.subTest(key=key, value=value):
                data = {key: value}
                response = self.client.patch(
                    reverse("enrollment", kwargs={"pk": 99}), data=data
                )

                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_enrollment(self):
        previous_number_enrollments = Enrollment.objects.all().count()

        response = self.client.delete(
            reverse("enrollment", kwargs={"pk": self.enroll_b.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Enrollment.objects.all().count(), previous_number_enrollments - 1
        )

    def test_delete_nonexistent_course(self):
        previous_number_enrollments = Enrollment.objects.all().count()

        response = self.client.delete(reverse("enrollment", kwargs={"pk": 99}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Enrollment.objects.all().count(), previous_number_enrollments)


class TestStudentAPI(APITestCase):
    invalid_student = {
        "avatar": "wrong.jpg",
        "name": 300 * "x",
        "nickname": 300 * "y",
        "phone": 9999999999999999,
    }
    required_fields = ["name", "nickname", "phone"]

    def setUp(self):
        self.student_a = Student.objects.create(
            name="Mock Silva", nickname="MS", phone="47999999999"
        )
        self.student_b = Student.objects.create(
            name="Mock Faria", nickname="MF", phone="47888888888"
        )
        self.student_c = Student.objects.create(
            name="Mock Pereira", nickname="MP", phone="476666666666"
        )

    def test_get_all_students(self):
        students = Student.objects.all()
        students_serialized = StudentSerializer(students, many=True)

        response = self.client.get(reverse("students"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data, students_serialized.data)

    def test_get_valid_single_student(self):
        student = Student.objects.get(pk=self.student_c.pk)
        student_serialized = StudentSerializer(student)

        response = self.client.get(reverse("student", kwargs={"pk": self.student_c.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data, student_serialized.data)

    def test_get_nonexistent_single_student(self):
        response = self.client.get(reverse("student", kwargs={"pk": 99}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(response.data, dict)

    def test_post_create_valid_student(self):
        previous_number_students = Student.objects.all().count()
        data = {"name": "Mock Junior", "nickname": "MJ", "phone": "47555555555"}

        response = self.client.post(reverse("students"), data)
        result = Student.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.all().count(), previous_number_students + 1)
        self.assertEqual(data["name"], result.name)
        self.assertEqual(data["nickname"], result.nickname)
        self.assertEqual(data["phone"], result.phone)

    def test_post_create_invalid_student(self):
        previous_number_students = Student.objects.all().count()
        data = {"name": "Mock Junior", "nickname": "MJ", "phone": "47555555555"}

        for field in self.required_fields:
            with self.subTest(field=field):
                data.pop(field)
                response = self.client.post(reverse("students"), data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(
                    Student.objects.all().count(), previous_number_students
                )

    def test_put_update_valid_student(self):
        student = Student.objects.get(pk=self.student_c.pk)
        data = {
            "avatar": image_default(),
            "name": "Mock Junior",
            "nickname": "MJ",
            "phone": "47555555555",
        }

        self.assertNotEqual(student.name, data["name"])
        self.assertNotEqual(student.nickname, data["nickname"])
        self.assertNotEqual(student.phone, data["phone"])

        response = self.client.put(
            reverse("student", kwargs={"pk": self.student_c.pk}), data=data
        )
        result = Student.objects.last()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.name, data["name"])
        self.assertEqual(result.nickname, data["nickname"])
        self.assertEqual(result.phone, data["phone"])

    def test_put_update_invalid_student(self):
        response = self.client.put(
            reverse("student", kwargs={"pk": self.student_c.pk}),
            data=self.invalid_student,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_update_nonexistent_student(self):
        data = {
            "avatar": image_default(),
            "name": "Mock Junior",
            "nickname": "MJ",
            "phone": "47555555555",
        }

        response = self.client.put(reverse("student", kwargs={"pk": 99}), data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_update_valid_student(self):
        update_data = {
            "avatar": image_default(),
            "name": "Mock Junior",
            "nickname": "MJ",
            "phone": "47555555555",
        }

        for key, value in update_data.items():
            with self.subTest(key=key, value=value):
                data = {key: value}
                response = self.client.patch(
                    reverse("student", kwargs={"pk": self.student_c.pk}), data=data
                )

                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_update_invalid_course(self):
        for key, value in self.invalid_student.items():
            with self.subTest(key=key, value=value):
                data = {key: value}
                response = self.client.patch(
                    reverse("student", kwargs={"pk": self.student_c.pk}), data=data
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_update_nonexistent_course(self):
        for key, value in self.invalid_student.items():
            with self.subTest(key=key, value=value):
                data = {key: value}
                response = self.client.patch(
                    reverse("student", kwargs={"pk": 99}), data=data
                )

                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_student(self):
        previous_number_students = Student.objects.all().count()

        response = self.client.delete(
            reverse("student", kwargs={"pk": self.student_c.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.all().count(), previous_number_students - 1)

    def test_delete_nonexistent_student(self):
        previous_number_students = Student.objects.all().count()

        response = self.client.delete(reverse("student", kwargs={"pk": 99}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Student.objects.all().count(), previous_number_students)
