from rest_framework import serializers #import serializers module from rest_framework, used to convert model instances to JSON and vice versa.
from .models import CustomUser, InternshipPlacement, WeeklyLog, EvaluationCriteria, Evaluation #import the models we created to be serialized.

class UserSerializer(serializers.ModelSerializer):#modelserializer generates fields from the model.
    class Meta:#specifies what model to serialize, which fields to include in the json
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']#exclude password for security.
        
class PlacementSerializer(serializers.ModelSerializer):
     class Meta:
           model = InternshipPlacement
           fields = '__all__' #include every field in the model.
     def validate_supervisor(self, value):
          if value.role != 'workplace_supervisor':#check if the user assigned as supervisor has the correct role.
               raise serializers.ValidationError('This user is not a supervisor.')#if not, raise an error.
          return value
class WeeklyLogSerializer(serializers.ModelSerializer):
     class Meta:
          model = WeeklyLog
          fields = '__all__'
          read_only_fields = ['submitted_at', 'created_at']#only set by django, not user input, so set to read only.
     def validate_status(self, value):
          request = self.context.get('request')
          if request and request.method == 'POST':#status must be draft on creation
               if value != 'draft':
                    raise serializers.ValidationError('New logs are created as draft only.')
          return value
class EvaluationCriteriaSerializer(serializers.ModelSerializer):
     class Meta:
          model = EvaluationCriteria
          fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Evaluation
            fields = '__all__'
            read_only_fields = ['created_at']
