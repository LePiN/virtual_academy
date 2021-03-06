# Generated by Django 3.2.7 on 2021-10-01 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("description", models.TextField(blank=True, default="")),
                ("duration", models.DurationField()),
                ("holder_image", models.ImageField(upload_to="")),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Curso",
                "verbose_name_plural": "Cursos",
            },
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("avatar", models.ImageField(upload_to="")),
                ("name", models.CharField(max_length=255)),
                ("nickname", models.CharField(max_length=25)),
                ("phone", models.CharField(max_length=12)),
            ],
            options={
                "verbose_name": "Aluno",
                "verbose_name_plural": "Alunos",
            },
        ),
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("date_close", models.DateField(blank=True, null=True)),
                ("date_enroll", models.DateField(auto_now_add=True)),
                (
                    "score",
                    models.DecimalField(
                        blank=True, decimal_places=1, max_digits=2, null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("AN", "Andamento"),
                            ("AP", "Aprovado"),
                            ("RE", "Reprovado"),
                        ],
                        default="AN",
                        max_length=2,
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="matriculas",
                        to="e_campus.course",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="matriculas",
                        to="e_campus.student",
                    ),
                ),
            ],
            options={
                "verbose_name": "Matricula",
                "verbose_name_plural": "Matriculas",
            },
        ),
    ]
