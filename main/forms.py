from django import forms
from django.contrib.auth.models import User, Group
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
    
    include_all_users = forms.BooleanField(
        required=False,
        initial=True,
        label="Assign to ALL active users (Uncheck to select specific people/groups)"
    )
    
    specific_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
        label="Select Specific Users"
    )

    specific_groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
        label="Select Specific Groups"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.FREQUENCY_CHOICES = [
            'Daily', 'Weekly', 'Monthly', 'Quarterly', 
            'Yearly', 'Seasonal', 'Weekly (Seasonal)'
        ]
        
        # Build a checkbox and an input box for every frequency option
        for freq in self.FREQUENCY_CHOICES:
            # Create a HTML name
            safe_name = freq.lower().replace(' ', '_').replace('(', '').replace(')', '')
            
            # The Checkboxs
            self.fields[f'chk_{safe_name}'] = forms.BooleanField(
                required=False, 
                label=freq,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input freq-checkbox'})
            )
            
            # The Number Inputs
            self.fields[f'count_{safe_name}'] = forms.IntegerField(
                required=False, 
                min_value=1, 
                initial=1,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control form-control-sm freq-count', 
                    'disabled': 'true', 
                    'style': 'width: 80px;'
                })
            )

# This method is used in the HTML template to loop through the frequencies 
# and display their checkboxes and count inputs together
    def get_frequency_fields(self):
        """Helper method so the HTML template can easily loop through these pairs"""
        fields = []
        for freq in self.FREQUENCY_CHOICES:
            safe_name = freq.lower().replace(' ', '_').replace('(', '').replace(')', '')
            fields.append({
                'name': freq,
                'checkbox': self[f'chk_{safe_name}'],
                'count': self[f'count_{safe_name}']
            })
        return fields

    # This method is called in the view after form validation 
    # to get a clean dictionary of just the selected frequencies and their counts
    def get_selected_frequencies(self):
        """Returns a dictionary for the View. Example: {'Daily': 3, 'Weekly': 1}"""
        selected = {}
        for freq in self.FREQUENCY_CHOICES:
            safe_name = freq.lower().replace(' ', '_').replace('(', '').replace(')', '')
            if self.cleaned_data.get(f'chk_{safe_name}'):
                count = self.cleaned_data.get(f'count_{safe_name}') or 1
                selected[freq] = count
        return selected