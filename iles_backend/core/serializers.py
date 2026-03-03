from rest_framework import serializers #import serializers module from rest_framework, used to convert model instances to JSON and vice versa.
from .models import CustomUser, InternshipPlacement, WeeklyLog, EvaluationCriteria, Evaluation #import the models we created to be serialized.

class UserSerializer(serializers.ModelSerializer):#modelserializer generates fields from the model.
    class Meta:#specifies what model to serialize, which fields to include in the jsoon
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']#exclude password for security.

class PlacementSerializer(serializers.ModelSerializer):
      class Meta:
           model = InternshipPlacement
           fields = '__all__' #include every field in the model.

class WeeklyLogSerializer(serializers.ModelSerializer):
     class Meta:
          model = WeeklyLog
          fields = '__all__'
          read_only_fields = ['submitted_at', 'created_at']#only set by django, not user input, so set to read only.

class EvaluationCriteriaSerializer(serializers.ModelSerializer):
     class Meta:
          model = EvaluationCriteria
          fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Evaluation
            fields = '__all__'
            read_only_fields = ['created_at']
