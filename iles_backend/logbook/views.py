from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import WeeklyLog
from .serializers import WeeklyLogSerializer
from users.permissions import IsStudent, IsSupervisor

class WeeklyLogViewSet(viewsets.ModelViewSet):
    queryset = WeeklyLog.objects.none()  # placeholder required by router; actual queryset is dynamic
    serializer_class = WeeklyLogSerializer

    def get_queryset(self):
        """Return logs based on the user's role."""
        user = self.request.user
        if user.role == 'student':
            return WeeklyLog.objects.filter(student=user)  # students see their own logs
        elif user.role in ['workplace_supervisor', 'academic_supervisor']:
            return WeeklyLog.objects.filter(placement__supervisor=user)  # supervisors see logs of their supervisees
        elif user.role == 'admin':
            return WeeklyLog.objects.all()
        return WeeklyLog.objects.none()

    def get_permissions(self):
        """
        - Only students can CREATE logs.
        - Only supervisors can UPDATE (PATCH/PUT) logs.
        - Anyone authenticated can VIEW (list/retrieve) based on get_queryset.
        """
        if self.action == 'create':
            return [IsStudent()]
        elif self.action in ['update', 'partial_update']:
            return [IsSupervisor()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """Force student to current user and status to 'draft'."""
        serializer.save(student=self.request.user, status='draft')
