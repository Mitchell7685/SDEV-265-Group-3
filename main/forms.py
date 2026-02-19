from django import forms
from .models import Chore


class ScheduleGeneratorForm(forms.Form):
    # Frequencies from Chore model
    FREQUENCY_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly'),
        ('Seasonal', 'Seasonal'),
        ('Weekly (Seasonal)', 'Weekly (Seasonal)')
    ]

    frequencies = forms.MultipleChoiceField(
        choices=FREQUENCY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Include Frequencies"
    )
    
    chores_per_user = forms.IntegerField(
        min_value=1, 
        initial=5,
        label="Number of Chores per User"
    )
    
    duration_days = forms.IntegerField(
        min_value=1,
        initial=7,
        label="Schedule Duration (in Days)",
        help_text="Used to calculate due dates."
    )

    include_admins = forms.BooleanField(
        required=False, 
        initial=False,
        label="Include Admins in Assignments"
    )

# Request extension
class ExtensionRequestForm(forms.Form):
    requested_due_date = forms.DateTimeField(
        label="Requested New Due Date and Time",
        help_text="When do you need this completed by?",
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False,
        label="Reason for Extension",
        help_text="Optional: Provide a reason for your request"
    )