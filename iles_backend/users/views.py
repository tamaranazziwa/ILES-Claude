from django.shortcuts import render
from rest_framework import viewsets, permissions  # lets us control who can access each endpoint
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()  # which records to work with: all users in database
    serializer_class = UserSerializer    # which serializer to use for converting to JSON
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users can access this endpoint
# Create your views here.
