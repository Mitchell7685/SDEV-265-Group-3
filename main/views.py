from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import AssignedChore, UserStats


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
    