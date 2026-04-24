from django.contrib.auth.models import AbstractUser  # built-in Django class with username, password...
from django.db import models  # module with all the known field types (CharField, DateField, ForeignKey)

class CustomUser(AbstractUser):  # a class that inherits from AbstractUser
    ROLE_CHOICES = [  # list of tuples: (stored_value, human_readable_value)
        ('student', 'Student Intern'),
        ('workplace_supervisor', 'Workplace Supervisor'),
        ('academic_supervisor', 'Academic Supervisor'),
        ('admin', 'Internship Administrator'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    # CharField is a text field, maximum 30 characters, only with the above choices

    def __str__(self):  # what shows up when you view the object in admin
        return f"{self.username} ({self.role})"