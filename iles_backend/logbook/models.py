from django.db import models
from django.conf import settings

class WeeklyLog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
    ]
    # log connected to student and placement; backtrack from user to logs with related_name='logs'
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logs')
    # placement uses a string reference ('placements.InternshipPlacement') to avoid circular imports
    placement = models.ForeignKey('placements.InternshipPlacement', on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()  # only positive whole numbers
    activities = models.TextField()  # longer character field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')  # set default status to draft
    submitted_at = models.DateTimeField(null=True, blank=True)  # can be blank because it's not submitted yet
    created_at = models.DateTimeField(auto_now_add=True)  # automatically set when created
    feedback = models.TextField(blank = True, default = '')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['student', 'week_number', 'placement'], 
                name='unique_weekly_log'
            )
        ]#one log per week

    def __str__(self):
        return f"Log Week {self.week_number} - {self.student.username}"