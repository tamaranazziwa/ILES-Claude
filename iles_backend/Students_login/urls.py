from rest_framework import viewsets, permissions
from .models import Issue
from .serializers import IssueSerializer 

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(intern=self.request.user)