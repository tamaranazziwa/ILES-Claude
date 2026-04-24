from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    """Allows access only to users with the 'student' role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsWorkplaceSupervisor(permissions.BasePermission):
    """Allows access only to users with the 'workplace_supervisor' role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'workplace_supervisor'

class IsAcademicSupervisor(permissions.BasePermission):
    """Allows access only to users with the 'academic_supervisor' role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'academic_supervisor'

class IsAdmin(permissions.BasePermission):
    """Allows access only to users with the 'admin' role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsSupervisor(permissions.BasePermission):
    """Allows access to both workplace and academic supervisors."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['workplace_supervisor', 'academic_supervisor']

class IsStudentOrSupervisor(permissions.BasePermission):
    """Allows access to students, supervisors, and admins (broad read permission)."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['student', 'workplace_supervisor', 'academic_supervisor', 'admin']