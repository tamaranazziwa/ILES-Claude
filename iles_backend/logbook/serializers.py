from rest_framework import serializers
from .models import WeeklyLog

class WeeklyLogSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()#read-only field calculated from related evaluations
    class Meta:
        model = WeeklyLog
        fields = '__all__'
        read_only_fields = ['student', 'submitted_at', 'created_at', 'total_score']  # these are set by the backend
    
    def get_total_score(self, obj):
        total =0.0
        for eval in obj.evaluations.all():
            total += eval.score * eval.criteria.weight
        return round(total, 2)