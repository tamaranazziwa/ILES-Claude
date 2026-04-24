from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlacementViewSet

router = DefaultRouter()
router.register(r'placements', PlacementViewSet)  # registers at /placements/

urlpatterns = [
    path('', include(router.urls)),
]