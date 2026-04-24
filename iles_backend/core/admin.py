from django.contrib import admin

# Register your models here.
from .models import (
    InternshipPlacement,
    WeeklyLog,
    EvaluationCriteria,
    Evaluation,
)

admin.site.register(InternshipPlacement)
admin.site.register(WeeklyLog)
admin.site.register(EvaluationCriteria)
admin.site.register(Evaluation)