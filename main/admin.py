from django.contrib import admin
from .models import Chore, AssignedChore, UserStats


# Chore Definition List (Menu)
@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ('chore_name', 'category', 'difficulty', 'default_points')
    list_filter = ('category', 'frequency', 'difficulty')
    search_fields = ('chore_name',)


# Assignment Manager (assign tasks)
@admin.register(AssignedChore)
class AssignedChoreAdmin(admin.ModelAdmin):
    list_display = ('chore_definition', 'assigned_to', 'date_due', 'is_completed', 'points_value')
    list_filter = ('is_completed', 'assigned_to', 'date_due')
    list_editable = ('is_completed',) 
    search_fields = ('assigned_to__username', 'chore_definition__chore_name')


# User Stats Viewer
@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill_level', 'experience_points', 'reward_points')
    