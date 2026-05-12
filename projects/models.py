from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db import models
from django.db.models import TextChoices
from pgvector.django import HnswIndex, VectorField


class ProjectStatus(TextChoices):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class Priority(TextChoices):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Project(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="projects",
        db_index=True,
    )
    name = models.CharField(max_length=200)
    goal = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.ACTIVE,
        db_index=True,
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True,
    )
    time_commitment = models.CharField(max_length=100, blank=True, default="")
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    stale_threshold_days = models.IntegerField(default=7)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    color = models.CharField(max_length=7, default="#E8553A")
    last_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    notes = models.TextField()
    duration_minutes = models.IntegerField(null=True, blank=True)
    mood = models.IntegerField(null=True, blank=True)  # 1-5
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    date = models.DateField()
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            HnswIndex(
                name="session_embedding_hnsw",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            ),
            GinIndex(
                name="session_search_vector_gin",
                fields=["search_vector"],
            ),
        ]

    def __str__(self):
        return f"{self.project.name} — {self.date}"


class Milestone(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="milestones",
    )
    name = models.CharField(max_length=200)
    target_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
