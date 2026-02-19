from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import AssignedChore, UserStats, ChoreExtensionRequest
from django.utils import timezone
from datetime import timedelta
import random

from .models import Chore, AssignedChore
from .forms import ScheduleGeneratorForm, ExtensionRequestForm
from django.shortcuts import get_object_or_404


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
    # Get the user's chores (if any exist yet) with related extension requests
    my_chores = AssignedChore.objects.filter(
        assigned_to=request.user, 
        is_completed=False
    ).prefetch_related('extension_requests')

    # Add a helper flag for each chore
    for chore in my_chores:
        chore.has_pending_extension = chore.extension_requests.filter(status='pending').exists()
        chore.latest_extension = chore.extension_requests.order_by('-requested_at').first()

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

# extention request 
@login_required
def request_extension(request, chore_id):
    assigned_chore = get_object_or_404(AssignedChore, id=chore_id, assigned_to=request.user)
    
    # Check if already completed
    if assigned_chore.is_completed:
        messages.error(request, "Cannot request extension for completed chore.")
        return redirect('home')
    
    # Check if already has a pending request
    if ChoreExtensionRequest.objects.filter(assigned_chore=assigned_chore, status='pending').exists():
        messages.warning(request, "You already have a pending extension request for this chore.")
        return redirect('home')
    
    if request.method == 'POST':
        form = ExtensionRequestForm(request.POST)
        if form.is_valid():
            requested_due_date = form.cleaned_data['requested_due_date']
            reason = form.cleaned_data['reason']
            
            # Validate that requested date is after current date
            if requested_due_date <= timezone.now():
                messages.error(request, "Requested due date must be in the future.")
                return render(request, 'extension_request.html', {
                    'form': form,
                    'assigned_chore': assigned_chore
                })
            
            # Create the extension request
            ChoreExtensionRequest.objects.create(
                assigned_chore=assigned_chore,
                requested_by=request.user,
                requested_due_date=requested_due_date,
                reason=reason
            )
            messages.success(request, f"Extension request submitted for {requested_due_date.strftime('%b %d, %Y %I:%M %p')}! Pending admin approval.")
            return redirect('home')
    else:
        # Pre-fill form with current due date + some default time
        initial_date = assigned_chore.date_due if assigned_chore.date_due else timezone.now() + timedelta(days=7)
        form = ExtensionRequestForm(initial={'requested_due_date': initial_date})
    
    return render(request, 'extension_request.html', {
        'form': form,
        'assigned_chore': assigned_chore
    })

@staff_member_required
def manage_extensions(request):
    pending_requests = ChoreExtensionRequest.objects.filter(status='pending')
    
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')  # 'approve' or 'reject'
        
        ext_request = get_object_or_404(ChoreExtensionRequest, id=request_id)
        
        if action == 'approve':
            # Set the new due date to what the user requested
            new_due_date = ext_request.requested_due_date
            
            ext_request.assigned_chore.date_due = new_due_date
            ext_request.assigned_chore.save()  # Save the chore first
            
            ext_request.status = 'approved'
            ext_request.reviewed_by = request.user
            ext_request.reviewed_at = timezone.now()
            ext_request.save()  # Then save the extension request
            
            messages.success(request, f"Extension approved! New due date: {new_due_date.strftime('%b %d, %Y %I:%M %p')}")
        
        elif action == 'reject':
            ext_request.status = 'rejected'
            ext_request.reviewed_by = request.user
            ext_request.reviewed_at = timezone.now()
            ext_request.save()
            messages.warning(request, "Extension rejected!")
        
        return redirect('manage_extensions')
    
    return render(request, 'manage_extensions.html', {'pending_requests': pending_requests})