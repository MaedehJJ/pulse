from rest_framework import serializers
from projects.models import Project, Session, Milestone


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ["id", "name", "target_date", "is_completed", "completed_at", "created_at"]
        read_only_fields = ["completed_at", "created_at"]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            "id", "project", "notes", "duration_minutes",
            "mood", "cost", "date", "created_at"
        ]
        read_only_fields = ["created_at", "embedding", "search_vector"]


class ProjectSerializer(serializers.ModelSerializer):
    milestones = MilestoneSerializer(many=True, read_only=True)
    session_count = serializers.SerializerMethodField()
    total_time_spent = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "name", "goal", "status", "priority",
            "time_commitment", "budget", "deadline",
            "stale_threshold_days", "tags", "color",
            "last_activity", "created_at", "updated_at",
            "milestones", "session_count", "total_time_spent"
        ]
        read_only_fields = ["last_activity", "created_at", "updated_at"]

    def get_session_count(self, obj):
        return obj.sessions.count()

    def get_total_time_spent(self, obj):
        from django.db.models import Sum
        result = obj.sessions.aggregate(total=Sum("duration_minutes"))
        return result["total"] or 0