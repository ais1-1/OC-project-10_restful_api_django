from django.db import models
from django.conf import settings


class Project(models.Model):
    BACKEND = "BACKEND"
    FRONTEND = "FRONTEND"
    IOS = "IOS"
    ANDROID = "ANDROID"

    TYPE_CHOICES = (
        (BACKEND, "Back-end"),
        (FRONTEND, "Front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    )

    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    project_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="authors",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.author:
            author_as_contributor = Contributor.objects.create(user=self.author)
            author_as_contributor.project.add(self)
            author_as_contributor.save()


class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributor",
    )
    project = models.ManyToManyField("Project", related_name="contributing")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
