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