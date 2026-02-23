from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import random

from django import forms
from django.forms import modelformset_factory

from .models import Chore, AssignedChore, UserStats
from .forms import ScheduleGeneratorForm


# Registration View
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save new user
            user = form.save()
            
            # Log in now
            login(request, user)
            
            # Redirect to homepage
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})


# Home view
@login_required 
def home(request):
    # Get the user's chores (if any exist yet)
    my_chores = AssignedChore.objects.filter(
        assigned_to=request.user, 
        is_completed=False
    )

    # Get the user's stats
    try:
        stats = request.user.userstats
    except UserStats.DoesNotExist:
        stats = None

    return render(request, "home.html", {
        "chores": my_chores,
        "stats": stats
    })


# Admin-only view to generate a new schedule of chores for users 
@staff_member_required
def generate_schedule(request):
    draft_ids = request.session.get('draft_schedule_ids', [])
    
    # Build the Formset Factory 
    DraftFormSet = modelformset_factory(
        AssignedChore,
        fields=('chore_definition', 'assigned_to', 'points_value', 'date_due'),
        can_delete=True,
        extra=0,
        widgets={
            'chore_definition': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'points_value': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'}),
            'date_due': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    )

    # Handle form submissions
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'generate':
            form = ScheduleGeneratorForm(request.POST)
            if form.is_valid():
                duration_days = form.cleaned_data['duration_days']
                
                 
                include_all = form.cleaned_data.get('include_all_users', False)
                
                if include_all:
                    users = User.objects.filter(is_active=True)
                else:
                    selected_users = form.cleaned_data.get('specific_users', User.objects.none())
                    selected_groups = form.cleaned_data.get('specific_groups', Group.objects.none())
                    users_in_groups = User.objects.filter(groups__in=selected_groups, is_active=True)
                    users = (selected_users | users_in_groups).distinct()
                
                if not users.exists():
                    messages.error(request, "You must select at least one user or group!")
                    return redirect('generate_schedule')

                
                selected_frequencies = form.get_selected_frequencies()
                
                if not selected_frequencies:
                    messages.error(request, "You must select at least one frequency category!")
                    return redirect('generate_schedule')

                
                eligible_chores_by_freq = {}
                for freq, count in selected_frequencies.items():
                    chores = list(Chore.objects.filter(frequency=freq))
                    if len(chores) < count:
                        messages.error(request, f"Only found {len(chores)} '{freq}' chores, but you requested {count}!")
                        return redirect('generate_schedule')
                    eligible_chores_by_freq[freq] = chores

                current_time = timezone.now()
                calculated_due_date = current_time + timedelta(days=duration_days)
                new_assignment_ids = []

                # The Assignment Loop
                for user in users:
                    for freq, count in selected_frequencies.items():
                        selected_chores = random.sample(eligible_chores_by_freq[freq], count)
                        
                        for chore in selected_chores:
                            new_assignment = AssignedChore.objects.create(
                                chore_definition=chore,
                                assigned_to=user,
                                is_completed=False,                     
                                date_assigned=current_time,             
                                date_due=calculated_due_date,           
                                points_value=chore.default_points       
                            )
                            new_assignment_ids.append(new_assignment.id)
                
                request.session['draft_schedule_ids'] = new_assignment_ids
                messages.success(request, "Draft generated! You can edit details below before finalizing.")
                return redirect('generate_schedule')

        elif action == 'confirm':
            formset = DraftFormSet(request.POST, queryset=AssignedChore.objects.filter(id__in=draft_ids))
            if formset.is_valid():
                formset.save()
                del request.session['draft_schedule_ids']
                messages.success(request, "Schedule finalized and saved to the database!")
                return redirect('admin:index')
            else:
                messages.error(request, "There was an error in your edits. Please check the table below.")
                
        elif action == 'cancel':
            AssignedChore.objects.filter(id__in=draft_ids).delete()
            del request.session['draft_schedule_ids']
            messages.info(request, "Draft schedule discarded.")
            return redirect('generate_schedule')

    
    generator_form = ScheduleGeneratorForm()
    formset = None

    if draft_ids:
        queryset = AssignedChore.objects.filter(id__in=draft_ids).order_by('date_due', 'assigned_to')
        if request.method != 'POST' or request.POST.get('action') != 'confirm':
            formset = DraftFormSet(queryset=queryset)

    return render(request, 'generate_schedule.html', {
        'form': generator_form,
        'formset': formset,
        'draft_ids': draft_ids 
    })


# Admin-only view to delete an assigned chore (used in the admin assigned chore list view)
@staff_member_required
def admin_delete_chore(request, chore_id):
    # Fetch the assignment
    assignment = get_object_or_404(AssignedChore, id=chore_id)
    
    if request.method == "POST":
        assignment.delete()
        messages.success(request, "Assignment removed successfully.")
        
    # Redirect back to the AssignedChore admin list
    return redirect('admin:main_assignedchore_changelist')
    

@login_required
def complete_chore(request, assignment_id):
    if request.method == "POST":
        # Get the chore, ensure it belongs to the user trying to complete it
        assignment = get_object_or_404(AssignedChore, id=assignment_id, assigned_to=request.user)
        
        # Prevent double-clicking or refreshing from awarding points twice
        if not assignment.is_completed:
            assignment.is_completed = True
            assignment.save()
            
            # Get the user's stats or create if they don't exist yet
            stats, created = UserStats.objects.get_or_create(user=request.user)
            
            # Add the XP and check for a level up
            leveled_up = stats.add_experience(assignment.points_value)
            
            if leveled_up:
                messages.success(request, f"Great Work! You earned {assignment.points_value} XP. New Skill Level Reached! You are now Level {stats.skill_level}!")
            else:
                messages.success(request, f"Great Work! You earned {assignment.points_value} XP.")
                
    return redirect('home')