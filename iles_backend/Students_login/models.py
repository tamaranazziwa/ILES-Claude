from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Issue(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    intern = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues_logged')
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues_assigned')
    date_logged = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(null=True, blank=True)
    internship = models.ForeignKey('internships.Internship', on_delete=models.CASCADE, related_name='issues')
    
    class Meta:
        ordering = ['-date_logged']
        
    def __str__(self):
        return f"{self.title} - {self.status}"