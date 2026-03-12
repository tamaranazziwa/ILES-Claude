from django.contrib.auth.models import AbstractUser #built in django class with username, password...
from django.db import models #moduls with all the known fieldtypes (CharField, DateField, ForeignKey)

class CustomUser(AbstractUser): #a class that inherits from AbstractUser
    ROLE_CHOICES = [#list of tuples, (stored_value, human_value)
        ('student', 'Student Intern'),
        ('workplace_supervisor', 'Workplace Supervisor'),
        ('academic_supervisor', 'Academic Supervisor'),
        ('admin', 'Internship Administrator'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    #CharField is a text field, maximum 30, only wih the above choices
    def __str__(self):#what shows up when you view the object in admin
        return f"{self.username} ({self.role})"


class InternshipPlacement(models.Model):#inherits from modles.Model, the base class for every django model.
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='placements')#ForeignKey creates a many to one relationship, delete everything when deleted, related_name lets you go back from a user to placements
    supervisor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='placement_supervisor', null=True) #supervisor is also a user, but with different role, related_name is different to avoid conflict.
    company_name = models.CharField(max_length=200)
    start_date = models.DateField()#stores a date
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)#stores date and time

    def __str__(self):
        return f"{self.student.username} at {self.company_name}, Supervisor- {self.supervisor.username}"


class WeeklyLog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
    ]
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='logs')#log connected to student and placement, backtrack from user to log.
    placement = models.ForeignKey(InternshipPlacement, on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()#only posititve whole numbers.
    activities = models.TextField()#longer character field.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')#set default status to draft.
    submitted_at = models.DateTimeField(null=True, blank=True)#can be blank because it is not submitted yet.
    created_at = models.DateTimeField(auto_now_add=True)#automatically set when created.

    def __str__(self):
        return f"Log Week {self.week_number} - {self.student.username}"


class EvaluationCriteria(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()  # e.g. 0.4 for 40%, add up to 1 accross all, stores decimal numbers.

    def __str__(self):
        return f"{self.name} ({self.weight * 100}%)"


class Evaluation(models.Model):
    log = models.ForeignKey(WeeklyLog, on_delete=models.CASCADE, related_name='evaluations')
    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    criteria = models.ForeignKey(EvaluationCriteria, on_delete=models.CASCADE)#connects person evaluating,log, and specific criteria.
    score = models.FloatField()
    comment = models.TextField(blank=True)#not NULL because empty string preffered over Null.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Eval by {self.evaluator.username} on {self.log}"
