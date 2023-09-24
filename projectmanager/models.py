import uuid
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
    description = models.CharField(blank=True, max_length=5000)
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


class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributor",
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="contributing"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ensures we don't get multiple Contributor instances
        # for unique user-project pairs
        # As unique_together will be deprecated in the future
        # using constraints instead (ref Django documentation)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "project"], name="unique_user_project_pairs"
            )
        ]

    def __str__(self):
        return self.user.username


class Issue(models.Model):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

    PRIORITY_CHOICES = (
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    )

    BUG = "BUG"
    FEATURE = "FEATURE"
    TASK = "TASK"

    TICKET_CHOICES = (
        (BUG, "Bug"),
        (FEATURE, "Feature"),
        (TASK, "Task"),
    )

    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"

    STATUS_CHOICES = (
        (TO_DO, "To do"),
        (IN_PROGRESS, "In progress"),
        (FINISHED, "Finished"),
    )

    name = models.CharField(max_length=250)
    description = models.CharField(blank=True, max_length=5000)
    author = models.ForeignKey(
        Contributor, on_delete=models.SET_NULL, null=True, related_name="author_issue"
    )
    assigned_to = models.ForeignKey(
        Contributor, on_delete=models.SET_NULL, null=True, related_name="has_issue"
    )
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    ticket = models.CharField(max_length=50, choices=TICKET_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=TO_DO)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="has_issue"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=5000)
    author = models.ForeignKey(
        Contributor, on_delete=models.SET_NULL, null=True, related_name="author_comment"
    )
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name="comment_of"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
