from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet

from projects.models import Milestone, Project, Session
from projects.serializers import (
    MilestoneSerializer,
    ProjectSerializer,
    SessionSerializer,
)


# Create your views here.
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }
        )


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users only see their own projects
        return (
            Project.objects.filter(user=self.request.user)
            .prefetch_related("milestones")
            .order_by("-updated_at")
        )

    def perform_create(self, serializer):
        # Automatically set user on creation
        serializer.save(user=self.request.user)


class SessionViewSet(ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Session.objects.filter(project__user=self.request.user).order_by("-date")

    def get_queryset_for_project(self, project_id):
        return self.get_queryset().filter(project_id=project_id)


class MilestoneViewSet(ModelViewSet):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Milestone.objects.filter(project__user=self.request.user).order_by(
            "target_date"
        )
