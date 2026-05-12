from dataclasses import dataclass, field


@dataclass
class DayPattern:
    day: str
    avg_mood: float
    avg_duration_minutes: float
    session_count: int


@dataclass
class WorkingPatterns:
    best_days: list[str] = field(default_factory=list)
    worst_days: list[str] = field(default_factory=list)
    day_breakdown: list[dict] = field(
        default_factory=list
    )  # list of DayPattern as dicts


@dataclass
class HourPeak:
    hour: int
    avg_mood: float
    session_count: int


@dataclass
class ProductivityPeaks:
    best_hours: list[int] = field(default_factory=list)
    hour_breakdown: list[dict] = field(
        default_factory=list
    )  # list of HourPeak as dicts


@dataclass
class ObstacleEntry:
    description: str
    frequency: int
    last_seen: str
    related_projects: list[str] = field(default_factory=list)


@dataclass
class ObstaclesLog:
    obstacles: list[dict] = field(
        default_factory=list
    )  # list of ObstacleEntry as dicts


@dataclass
class ProjectStreak:
    project_id: int
    project_name: str
    current_streak_days: int
    best_streak_days: int
    last_session_date: str


@dataclass
class StreakData:
    projects: list[dict] = field(default_factory=list)  # list of ProjectStreak as dicts
    overall_current_streak: int = 0
    overall_best_streak: int = 0


@dataclass
class InsightContext:
    """Context passed to the AI when generating an insight."""

    user_id: int
    project_names: list[str] = field(default_factory=list)
    avg_session_duration: int | None = None
    best_days: list[str] = field(default_factory=list)
    recent_obstacles: list[str] = field(default_factory=list)
    project_completion_rate: float | None = None
