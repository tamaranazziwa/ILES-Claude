# import the models  

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    InternshipPlacement,
    WeeklyLog,
    EvaluationCriteria,
    Evaluation,
)
from .serializer import (
    InternshipPlacementSerializer,
    WeeklyLogSerializer,
    EvaluationCriteriaSerializer,
    EvaluationSerializer,
)

class InternshipPlacementViewSet(viewsets.ModelViewSet):
    """Full CRUD for placements with role-based access (permissions added in next step)."""
    queryset = InternshipPlacement.objects.all()
    serializer_class = InternshipPlacementSerializer
    permission_classes = [permissions.IsAuthenticated]

class WeeklyLogViewSet(viewsets.ModelViewSet):
    queryset = WeeklyLog.objects.all()
    serializer_class = WeeklyLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class EvaluationCriteriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EvaluationCriteria.objects.all()
    serializer_class = EvaluationCriteriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def compute_score(self, request, pk=None):
        """Placeholder for weighted score computation (implemented fully in Week 9)."""
        evaluation = self.get_object()
        # Future weighted logic will be added here
        return Response({"message": "Score computation placeholder", "score": evaluation.score})