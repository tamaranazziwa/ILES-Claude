
from rest_framework import permissions

class IsStudentIntern(permissions.BasePermission):
    """Only Student Interns may create or list their own placements."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student_intern'

class IsSupervisorOrAdmin(permissions.BasePermission):
    """Workplace/Academic Supervisors and Administrators may view and manage placements."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            'workplace_supervisor', 'academic_supervisor', 'internship_administrator'
        ]

class IsPlacementOwnerOrSupervisor(permissions.BasePermission):
    """Students may only edit their own placements; supervisors may review any."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'student_intern':
            return obj.student == request.user
        return request.user.role in ['workplace_supervisor', 'academic_supervisor', 'internship_administrator']