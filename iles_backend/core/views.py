from rest_framework import viewsets, permissions #lets us control who can access each endpoint.(ModelViewSeet.permissions)
from .models import CustomUser, InternshipPlacement, WeeklyLog, EvaluationCriteria, Evaluation
from .serializers import UserSerializer, PlacementSerializer, WeeklyLogSerializer,EvaluationCriteriaSerializer, EvaluationSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()#which records to work with, allusers in database
    serializer_class = UserSerializer#which serializer to use for converting to JSON
    permission_classes = [permissions.IsAuthenticated]#only logged in users can access this endpoint.

class PlacementViewSet(viewsets.ModelViewSet):
    queryset = InternshipPlacement.objects.all()
    serializer_class = PlacementSerializer
    permission_classes = [permissions.IsAuthenticated]

class WeeklyLogViewSet(viewsets.ModelViewSet):
    queryset = WeeklyLog.objects.all()
    serializer_class = WeeklyLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class EvaluationCriteriaViewSet(viewsets.ModelViewSet):
    queryset = EvaluationCriteria.objects.all()
    serializer_class = EvaluationCriteriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

#a view is a class that recieves request from react does something with database and sends back a response.
