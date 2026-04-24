from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()  # creates a router object that automatically generates URLs for viewsets
router.register(r'users', UserViewSet)  # registers viewset at the /users/ path (r for raw string)

urlpatterns = [
    path('', include(router.urls)),  # router generates all the URL patterns automatically
]