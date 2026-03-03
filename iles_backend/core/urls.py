from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()#creates a router object that automatically generates URLs for viewsets.
router.register(r'users', views.UserViewSet)#registers viewset at the logs/path.(r for rawstring)
router.register(r'placements', views.PlacementViewSet)
router.register(r'logs', views.WeeklyLogViewSet)
router.register(r'criteria', views.EvaluationCriteriaViewSet)
router.register(r'evaluations', views.EvaluationViewSet)

urlpatterns = [
    path('', include(router.urls)),#router generates all the URL patterns automatically and includes in urlpatterns.
]