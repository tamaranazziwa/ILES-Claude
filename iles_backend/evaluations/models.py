from django.db import models
from django.db import models
from django.conf import settings

class EvaluationCriteria(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()  # e.g., 0.4 for 40% (should add up to 1 across all criteria)

    def __str__(self):
        return f"{self.name} ({self.weight * 100}%)"


class Evaluation(models.Model):
    # connects person evaluating, log, and specific criteria
    log = models.ForeignKey('logbook.WeeklyLog', on_delete=models.CASCADE, related_name='evaluations')
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    criteria = models.ForeignKey(EvaluationCriteria, on_delete=models.CASCADE)
    score = models.FloatField()
    comment = models.TextField(blank=True)  # blank=True means empty string is allowed (preferred over null)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Eval by {self.evaluator.username} on {self.log}"
# Create your models here.
