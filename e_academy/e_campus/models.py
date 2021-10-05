from django.db import models


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(BaseModel):
    description = models.TextField()
    duration = models.DurationField()
    holder_image = models.ImageField(blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.name


class Student(BaseModel):
    avatar = models.ImageField(blank=True)
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=25)
    phone = models.CharField(max_length=12)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return self.name


class Enrollment(BaseModel):
    ANDAMENTO = "AN"
    APROVADO = "AP"
    REPROVADO = "RE"
    STATUS_CHOICES = [
        (ANDAMENTO, "Andamento"),
        (APROVADO, "Aprovado"),
        (REPROVADO, "Reprovado"),
    ]

    course = models.ForeignKey(
        Course, related_name="matriculas", on_delete=models.PROTECT
    )
    date_close = models.DateField(blank=True, null=True)
    date_enroll = models.DateField(auto_now_add=True)
    score = models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=ANDAMENTO,
    )
    student = models.ForeignKey(
        Student, related_name="matriculas", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Matricula"
        verbose_name_plural = "Matriculas"

    def __str__(self):
        return f"{self.student.name}/{self.course.name}/{self.status}"
