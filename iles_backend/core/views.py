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
    
    
class InternshipPlacementViewSet(viewsets.ModelViewSet):
    """Full CRUD for Internship Placements with strict validation and RBAC."""
    queryset = InternshipPlacement.objects.all()
    serializer_class = InternshipPlacementSerializer
    
    def get_permissions(self):
        """Role-based permissions per action."""
        if self.action in ['create', 'list', 'retrieve']:
            if self.request.user.role == 'student_intern':
                return [IsStudentIntern()]
            return [IsSupervisorOrAdmin()]
        # Update and delete are restricted to owner or supervisor
        return [permissions.IsAuthenticated(), IsPlacementOwnerOrSupervisor()]

    @action(detail=False, methods=['get'])
    def my_placements(self, request):
        """Student-specific endpoint: list only their own placements."""
        placements = InternshipPlacement.objects.filter(student=request.user)
        serializer = self.get_serializer(placements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_supervisors(self, request, pk=None):
        """Custom action: assign workplace and academic supervisors (admin/supervisor only)."""
        placement = self.get_object()
        serializer = InternshipPlacementSerializer(placement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)