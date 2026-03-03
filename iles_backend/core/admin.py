from django.contrib import admin#imports django admin module
from django.contrib.auth.admin import UserAdmin#special admin class for user models, provides default fields and functionality for user management in admin.
from .models import CustomUser, InternshipPlacement, WeeklyLog, EvaluationCriteria, Evaluation
#from the same folder('.') import the models we created to be registered.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
        )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)#show model in admin panel. Use CustomUserAdmin to get the default user management features.
admin.site.register(InternshipPlacement)#uses default user admin panel.
admin.site.register(WeeklyLog)
admin.site.register(EvaluationCriteria)
admin.site.register(Evaluation)