from rest_framework import viewsets, permissions #lets us control who can access each endpoint.(ModelViewSeet.permissions)
from .models import CustomUser, InternshipPlacement, WeeklyLog, EvaluationCriteria, Evaluation
from .serializers import UserSerializer, PlacementSerializer, WeeklyLogSerializer,EvaluationCriteriaSerializer, EvaluationSerializer
from .permissions import IsStudent, IsSupervisor, IsWorkplaceSupervisor, IsAcademicSupervisor, IsAdmin, IsStudentOrSupervisor
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()#which records to work with, allusers in database
    serializer_class = UserSerializer#which serializer to use for converting to JSON
    permission_classes = [permissions.IsAuthenticated]#only logged in users can access this endpoint.

class PlacementViewSet(viewsets.ModelViewSet):
    queryset = InternshipPlacement.objects.none()#def overrides this when running
    serializer_class = PlacementSerializer
    permission_classes = [IsStudentOrSupervisor]#only students and supervisors can see placements, students only theirs

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return InternshipPlacement.objects.filter(student = user)
        elif user.role in ['workplace_supervisor', 'academic_supervisor']:
            return InternshipPlacement.objects.filter(supervisor = user)
        elif user.role == 'admin':
            return InternshipPlacement.objects.all()
        return InternshipPlacement.objects.none()#no access for others
        
class WeeklyLogViewSet(viewsets.ModelViewSet):
    queryset = WeeklyLog.objects.none()#def overrides this when running
    serializer_class = WeeklyLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return WeeklyLog.objects.filter(student = user)
        elif user.role in ['workplace_supervisor', 'academic_supervisor']:
            return WeeklyLog.objects.filter(placement__supervisor = user)
        elif user.role == 'admin':
            return WeeklyLog.objects.all()
        return WeeklyLog.objects.none()
    
    def get_permissions(self):
        if self.action == 'create':#only students create logs
            return [IsStudent()]
        elif self.action in ['update', 'partial_update']:#only supervisors can update status to reviewed
            return [IsSupervisor()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(student = self.request.user, status = 'draft')
class EvaluationCriteriaViewSet(viewsets.ModelViewSet):
    queryset = EvaluationCriteria.objects.all()
    serializer_class = EvaluationCriteriaSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.none()#def overrides this when running
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]
  
    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Evaluation.objects.filter(log__student=user)
        elif user.role in ['workplace_supervisor', 'academic_supervisor']:
            return Evaluation.objects.filter(log__placement__supervisor=user)
        elif user.role == 'admin':
            return Evaluation.objects.all()
        return Evaluation.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsSupervisor()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(evaluator = self.request.user)
#a view is a class that recieves request from react does something with database and sends back a response.
