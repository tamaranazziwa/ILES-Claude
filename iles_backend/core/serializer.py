from rest_framework import serializers
from .models import (
    InternshipPlacement,
    WeeklyLog,
    EvaluationCriteria,
    Evaluation,
)
from accounts.models import CustomUser

# InternshipPlacement Serializer
class InternshipPlacementSerializer(serializers.ModelSerializer):
    """
    Handles creation and validation of InternshipPlacement.
    Enforces date validation and overlap prevention (business rule).
    """
    student = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='student_intern'),
        required=True
    )
    workplace_supervisor = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='workplace_supervisor'),
        required=False,
        allow_null=True
    )
    academic_supervisor = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='academic_supervisor'),
        required=False,
        allow_null=True
    )

    class Meta:
        model = InternshipPlacement
        fields = [
            'id', 'student', 'workplace_supervisor', 'academic_supervisor',
            'company_name', 'start_date', 'end_date', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """Custom validation: prevent overlapping placements and invalid dates."""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        student = data.get('student')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("End date must be after start date.")

        # Overlap check (excludes the current instance if updating)
        existing = InternshipPlacement.objects.filter(
            student=student,
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exclude(pk=self.instance.pk if self.instance else None)

        if existing.exists():
            raise serializers.ValidationError(
                "Student already has an overlapping internship placement."
            )
        return data

#  WeeklyLog Serializer 
class WeeklyLogSerializer(serializers.ModelSerializer):
    placement = serializers.PrimaryKeyRelatedField(queryset=InternshipPlacement.objects.all())
    reviewed_by = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role__in=['workplace_supervisor', 'academic_supervisor']),
        required=False,
        allow_null=True
    )

    class Meta:
        model = WeeklyLog
        fields = [
            'id', 'placement', 'week_number', 'activities', 'achievements',
            'challenges', 'status', 'submitted_at', 'reviewed_by',
            'review_comments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['submitted_at', 'created_at', 'updated_at']

    def validate(self, data):
        """Enforce workflow state transitions (basic validation)."""
        if data.get('status') == 'approved' and not data.get('reviewed_by'):
            raise serializers.ValidationError("Approved logs must have a reviewer.")
        return data

# EvaluationCriteria Serializer 
class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriteria
        fields = ['id', 'name', 'weight', 'description', 'category']

# Evaluation Serializer 
class EvaluationSerializer(serializers.ModelSerializer):
    placement = serializers.PrimaryKeyRelatedField(queryset=InternshipPlacement.objects.all())
    evaluator = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(
        role__in=['workplace_supervisor', 'academic_supervisor', 'internship_administrator']
    ))
    criteria = serializers.PrimaryKeyRelatedField(queryset=EvaluationCriteria.objects.all())

    class Meta:
        model = Evaluation
        fields = [
            'id', 'placement', 'evaluator', 'criteria', 'score',
            'comments', 'evaluated_at'
        ]
        read_only_fields = ['evaluated_at']

    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Score must be between 0 and 100.")
        return value