from django.db import models  # module with all the known field types (CharField, DateField, ForeignKey)
from django.conf import settings  # to reference the custom user model

class InternshipPlacement(models.Model):  # inherits from models.Model, the base class for every Django model
    # ForeignKey creates a many-to-one relationship; on_delete=models.CASCADE deletes placement if student is deleted
    # related_name lets you go backward from user to placements (e.g., user.placements.all())
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='placements')
    # supervisor is also a user, but with a different role; related_name is different to avoid conflict
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='placement_supervisor', null=True)
    company_name = models.CharField(max_length=200)
    start_date = models.DateField()  # stores a date (year, month, day)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # stores date and time, automatically set when created

    def __str__(self):
        sup_name = self.supervisor.username if self.supervisor else 'None'
        return f"{self.student.username} at {self.company_name}, Supervisor- {sup_name}"