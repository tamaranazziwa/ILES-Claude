"""
URL configuration for iles_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter

from core.views import (
    InternshipPlacementViewSet,
    WeeklyLogViewSet,
    EvaluationCriteriaViewSet,
    EvaluationViewSet,
)

# DRF Router for all API endpoints
router = DefaultRouter()
router.register(r'placements', InternshipPlacementViewSet, basename='placement')
router.register(r'weekly-logs', WeeklyLogViewSet, basename='weekly-log')
router.register(r'evaluation-criteria', EvaluationCriteriaViewSet, basename='evaluation-criteria')
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')

# Root redirect to API (user-friendly landing)
def root_redirect(request):
    return redirect('/api/')

urlpatterns = [
    path('', root_redirect, name='root-redirect'),
    path('admin/', admin.site.urls),
    path('api/', include('router.urls')),
]
