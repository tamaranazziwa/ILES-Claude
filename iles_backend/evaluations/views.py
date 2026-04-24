from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import EvaluationCriteria, Evaluation
from .serializers import EvaluationCriteriaSerializer, EvaluationSerializer
from users.permissions import IsAdmin, IsSupervisor

class EvaluationCriteriaViewSet(viewsets.ModelViewSet):
    queryset = EvaluationCriteria.objects.all()
    serializer_class = EvaluationCriteriaSerializer

    def get_permissions(self):
        """Only admins can create/modify criteria; others can only read."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.none()  # placeholder
    queryset = Evaluation.objects.none()
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        """Students see evaluations on their logs; supervisors see evaluations they gave or on their supervisees."""
        user = self.request.user
        if user.role == 'student':
            return Evaluation.objects.filter(log__student=user)
        elif user.role in ['workplace_supervisor', 'academic_supervisor']:
            return Evaluation.objects.filter(log__placement__supervisor=user)
        elif user.role == 'admin':
            return Evaluation.objects.all()
        return Evaluation.objects.none()

    def get_permissions(self):
        """Only supervisors can create evaluations."""
        if self.action == 'create':
            return [IsSupervisor()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """Automatically set the evaluator to the logged-in user."""
        serializer.save(evaluator=self.request.user)
# Create your views here.
