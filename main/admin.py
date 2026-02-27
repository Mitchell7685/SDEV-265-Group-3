from django.contrib import admin
from django.utils.html import format_html
from .models import Chore, AssignedChore, UserStats, ChoreExtensionRequest


# Chore Definition List (Menu)
@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ('chore_name', 'category', 'frequency', 'difficulty', 'default_points')
    list_filter = ('category', 'frequency', 'difficulty')
    search_fields = ('chore_name',)


# Assignment Manager (assign tasks)
@admin.register(AssignedChore)
class AssignedChoreAdmin(admin.ModelAdmin):
    list_display = ('chore_definition', 'assigned_to', 'date_due', 'is_completed', 'points_value', 'remove_button')
    list_filter = ('is_completed', 'assigned_to', 'date_due')
    list_editable = ('is_completed',) 
    search_fields = ('assigned_to__username', 'chore_definition__chore_name')

    # This creates the trash can button for every row
    def remove_button(self, obj):
        return format_html(
            '<button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#deleteModal" '
            'onclick="setModalData({}, \'{}\')">'
            '<i class="fas fa-trash"></i></button>',
            obj.id, obj.chore_definition.chore_name
        )
    
    # Names the column "Remove" instead of "Remove Button"
    remove_button.short_description = 'Remove'


# User Stats Viewer
@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill_level', 'experience_points', 'reward_points')


# Extension Request Manager
@admin.register(ChoreExtensionRequest)
class ChoreExtensionRequestAdmin(admin.ModelAdmin):
    list_display = ('assigned_chore', 'requested_by', 'requested_due_date', 'status', 'requested_at', 'reviewed_by')
    list_filter = ('status', 'requested_at', 'reviewed_by')
    search_fields = ('requested_by__username', 'assigned_chore__chore_definition__chore_name')
    readonly_fields = ('requested_at', 'reviewed_at')
    