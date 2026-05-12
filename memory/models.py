import dataclasses

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db import models

from memory.schemas import ObstaclesLog, ProductivityPeaks, StreakData, WorkingPatterns


class UserMemory(models.Model):
    user = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="memory",
    )
    # Schema: WorkingPatterns
    working_patterns = models.JSONField(default=dict)

    # Schema: ProductivityPeaks
    productivity_peaks = models.JSONField(default=dict)

    avg_session_duration = models.IntegerField(null=True, blank=True)
    project_completion_rate = models.FloatField(null=True, blank=True)
    focus_areas = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    # Schema: ObstaclesLog
    obstacles_log = models.JSONField(default=dict)

    # Schema: StreakData
    streak_data = models.JSONField(default=dict)

    timezone = models.CharField(max_length=50, default="UTC")
    last_updated = models.DateTimeField(auto_now=True)

    def get_working_patterns(self) -> WorkingPatterns:
        return (
            WorkingPatterns(**self.working_patterns)
            if self.working_patterns
            else WorkingPatterns()
        )

    def set_working_patterns(self, patterns: WorkingPatterns) -> None:
        self.working_patterns = dataclasses.asdict(patterns)

    def get_productivity_peaks(self) -> ProductivityPeaks:
        return (
            ProductivityPeaks(**self.productivity_peaks)
            if self.productivity_peaks
            else ProductivityPeaks()
        )

    def set_productivity_peaks(self, peaks: ProductivityPeaks) -> None:
        self.productivity_peaks = dataclasses.asdict(peaks)

    def get_obstacles_log(self) -> ObstaclesLog:
        return (
            ObstaclesLog(**self.obstacles_log) if self.obstacles_log else ObstaclesLog()
        )

    def set_obstacles_log(self, log: ObstaclesLog) -> None:
        self.obstacles_log = dataclasses.asdict(log)

    def get_streak_data(self) -> StreakData:
        return StreakData(**self.streak_data) if self.streak_data else StreakData()

    def set_streak_data(self, streaks: StreakData) -> None:
        self.streak_data = dataclasses.asdict(streaks)

    def __str__(self):
        return f"Memory — {self.user.username}"

class InsightType(models.TextChoices):
    PATTERN = "pattern"
    WARNING = "warning"
    SUGGESTION = "suggestion"


class Insight(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="insights",
        db_index=True,
    )
    content = models.TextField()
    insight_type = models.CharField(
        max_length=20,
        choices=InsightType.choices,
        db_index=True,
    )
    related_project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="insights",
    )
    was_useful = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.insight_type} — {self.user.username}"
