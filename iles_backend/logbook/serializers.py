from rest_framework import serializers
from .models import WeeklyLog

class WeeklyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyLog
        fields = '__all__'
        read_only_fields = ['student', 'submitted_at', 'created_at']  # these are set by the backend
