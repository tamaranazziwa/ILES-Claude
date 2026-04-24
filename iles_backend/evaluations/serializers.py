from rest_framework import serializers
from .models import EvaluationCriteria, Evaluation

class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriteria
        fields = '__all__'


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
        read_only_fields = ['evaluator', 'created_at']  # set automatically by backend