from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvaluationCriteriaViewSet, EvaluationViewSet

router = DefaultRouter()
router.register(r'criteria', EvaluationCriteriaViewSet)  # /api/criteria/
router.register(r'evaluations', EvaluationViewSet)      # /api/evaluations/

urlpatterns = [
    path('', include(router.urls)),
]