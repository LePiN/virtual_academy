from django.contrib import admin

from .models import Course
from .models import Enrollment
from .models import Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "duration",
        "holder_image",
        "name",
        "date_created",
        "date_updated",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "date_close",
        "date_enroll",
        "score",
        "status",
        "student",
        "date_created",
        "date_updated",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "avatar",
        "name",
        "nickname",
        "phone",
        "date_created",
        "date_updated",
    )
