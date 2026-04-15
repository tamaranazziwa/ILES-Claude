from rest_framework import permissions

class IsStudent(permissions.BasePermission):#only students can access
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsWorkplaceSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'workplace_supervisor'

class IsAcademicSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'academic_supervisor'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsStudentOrSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['student', 'workplace_supervisor', 'academic_supervisor', 'admin']

class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['workplace_supervisor', 'academic_supervisor']    