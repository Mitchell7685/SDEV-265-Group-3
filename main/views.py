from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import AssignedChore, UserStats
from django.utils import timezone
from datetime import timedelta
import random

from .models import Chore, AssignedChore
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


@staff_member_required
def generate_schedule(request):
    if request.method == 'POST':
        form = ScheduleGeneratorForm(request.POST)
        
        if form.is_valid():
            frequencies = form.cleaned_data['frequencies']
            chores_per_user = form.cleaned_data['chores_per_user']
            duration_days = form.cleaned_data['duration_days']
            
            # Include admins or not
            include_admins = form.cleaned_data['include_admins']
            
            # Get the appropriate users based on the checkbox
            if include_admins:
                # Grab everyone who is active
                users = User.objects.filter(is_active=True)
            else:
                # Grab only non-admins
                users = User.objects.filter(is_superuser=False, is_active=True) 
            
            # Find all chores that match the checked frequency boxes
            eligible_chores = list(Chore.objects.filter(frequency__in=frequencies))
            
            # Make sure we actually have enough chores to assign
            if len(eligible_chores) < chores_per_user:
                messages.error(request, f"Only found {len(eligible_chores)} chores, but you requested {chores_per_user} per user!")
                return redirect('generate_schedule')

            # Calculate date
            current_time = timezone.now()
            calculated_due_date = current_time + timedelta(days=duration_days)

            # The Randomizer Loop
            for user in users:
                # Pick random unique chores for this specific user
                selected_chores = random.sample(eligible_chores, chores_per_user)
                
                for chore in selected_chores:
                    # Create the assignment
                    AssignedChore.objects.create(
                        chore_definition=chore,
                        assigned_to=user,
                        is_completed=False,                     
                        date_assigned=current_time,             
                        date_due=calculated_due_date,           
                        points_value=chore.default_points       
                    )
            
            messages.success(request, f"Successfully assigned {chores_per_user} chores to each user!")
            return redirect('admin:index') 

    else:
        form = ScheduleGeneratorForm()

    return render(request, 'generate_schedule.html', {'form': form})
    