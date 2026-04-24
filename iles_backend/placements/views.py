from django.shortcuts import render
from rest_framework import viewsets  # provides CRUD operations out of the box
from .models import InternshipPlacement
from .serializers import PlacementSerializer
from users.permissions import IsStudentOrSupervisor  # custom permission class

class PlacementViewSet(viewsets.ModelViewSet):
    serializer_class = PlacementSerializer
    queryset = InternshipPlacement.objects.none()
    permission_classes = [IsStudentOrSupervisor]  # only students and supervisors can see placements

    def get_queryset(self):
        """Return different queryset based on the logged-in user's role."""
        user = self.request.user
        if user.role == 'student':
            return InternshipPlacement.objects.filter(student=user)  # student sees only their own
        elif user.role in ['workplace_supervisor', 'academic_supervisor']:
            return InternshipPlacement.objects.filter(supervisor=user)  # supervisor sees placements they supervise
        elif user.role == 'admin':
            return InternshipPlacement.objects.all()  # admin sees everything
        return InternshipPlacement.objects.none()  # no access for others
# Create your views here.
