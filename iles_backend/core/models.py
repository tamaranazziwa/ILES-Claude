# Import neccessary models here
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from Students_login.models import CustomUser  # Import CustomUser for role-based FKs

# WORKFLOW STATE CHOICES (used by multiple models) 
LOG_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('submitted', 'Submitted'),
    ('reviewed', 'Reviewed'),
    ('approved', 'Approved'),
]

PLACEMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

# 1. InternshipPlacement Model 
class InternshipPlacement(models.Model):
    """
    Normalized placement record. One student can have only one active placement at a time.
    """
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='internship_placements',
        limit_choices_to={'role': 'student_intern'},
        verbose_name="Student Intern"
    )
    workplace_supervisor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_placements',
        limit_choices_to={'role': 'workplace_supervisor'},
        verbose_name="Workplace Supervisor"
    )
    academic_supervisor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='academic_supervised_placements',
        limit_choices_to={'role': 'academic_supervisor'},
        verbose_name="Academic Supervisor"
    )
    company_name = models.CharField(max_length=255, verbose_name="Company / Organization")
    start_date = models.DateField(verbose_name="Internship Start Date")
    end_date = models.DateField(verbose_name="Internship End Date")
    status = models.CharField(
        max_length=20,
        choices=PLACEMENT_STATUS_CHOICES,
        default='pending',
        verbose_name="Placement Status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Internship Placement"
        verbose_name_plural = "Internship Placements"
        # Prevent overlapping placements for the same student (business rule enforcement)
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'start_date', 'end_date'],
                name='unique_student_placement_dates'
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.company_name} ({self.start_date} to {self.end_date})"

    def clean(self):
        """Prevent overlapping date ranges for the same student."""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")
        # Additional overlap check will be implemented in serializer/view level for full enforcement.

# 2. WeeklyLog Model 
class WeeklyLog(models.Model):
    """
    Weekly activity log submitted by student. Linked 1:M to Placement.
    Enforces workflow states (Draft → Submitted → Reviewed → Approved).
    """
    placement = models.ForeignKey(
        InternshipPlacement,
        on_delete=models.CASCADE,
        related_name='weekly_logs',
        verbose_name="Internship Placement"
    )
    week_number = models.PositiveIntegerField(verbose_name="Week Number")
    activities = models.TextField(verbose_name="Activities Performed")
    achievements = models.TextField(blank=True, verbose_name="Key Achievements")
    challenges = models.TextField(blank=True, verbose_name="Challenges Faced")
    status = models.CharField(
        max_length=20,
        choices=LOG_STATUS_CHOICES,
        default='draft',
        verbose_name="Log Status"
    )
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name="Submission Timestamp")
    reviewed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role__in': ['workplace_supervisor', 'academic_supervisor']},
        verbose_name="Reviewed By"
    )
    review_comments = models.TextField(blank=True, verbose_name="Supervisor Review Comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Weekly Log"
        verbose_name_plural = "Weekly Logs"
        unique_together = ('placement', 'week_number')  # One log per week per placement

    def __str__(self):
        return f"Week {self.week_number} - {self.placement.student}"

# 3. EvaluationCriteria Model 
class EvaluationCriteria(models.Model):
    """
    Reusable, weighted evaluation criteria (supports automated scoring in later weeks).
    Example: Attendance (40%), Technical Skills (30%), Professionalism (30%).
    """
    name = models.CharField(max_length=100, verbose_name="Criteria Name")
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Weight (e.g., 0.40 for 40%)"
    )
    description = models.TextField(blank=True, verbose_name="Description")
    category = models.CharField(
        max_length=50,
        choices=[('supervisor', 'Workplace Supervisor'), ('academic', 'Academic Supervisor')],
        default='supervisor',
        verbose_name="Evaluator Category"
    )

    class Meta:
        verbose_name = "Evaluation Criteria"
        verbose_name_plural = "Evaluation Criteria"

    def __str__(self):
        return f"{self.name} ({self.weight * 100}%)"

# 4. Evaluation Model 
class Evaluation(models.Model):
    """
    Final/per-placement evaluation. Linked to Placement and Criteria.
    Supports weighted score computation (Week 9 requirement).
    """
    placement = models.ForeignKey(
        InternshipPlacement,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name="Internship Placement"
    )
    evaluator = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': ['workplace_supervisor', 'academic_supervisor', 'internship_administrator']},
        verbose_name="Evaluator"
    )
    criteria = models.ForeignKey(
        EvaluationCriteria,
        on_delete=models.PROTECT,
        verbose_name="Evaluation Criteria"
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Score (0-100)"
    )
    comments = models.TextField(blank=True, verbose_name="Evaluator Comments")
    evaluated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Evaluation"
        verbose_name_plural = "Evaluations"
        # Prevent duplicate evaluations for same placement + criteria + evaluator
        unique_together = ('placement', 'evaluator', 'criteria')

    def __str__(self):
        return f"{self.placement} - {self.criteria.name} by {self.evaluator}"

    def clean(self):
        if self.score < 0 or self.score > 100:
            raise ValidationError("Score must be between 0 and 100.")