import os
import csv
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.utils import timezone


# ---------------- USER STATS ---------------------
class UserStats(models.Model):
    # Connects stats to one specific Login User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Attributes
    name = models.CharField(max_length=100) 
    age = models.IntegerField(null=True, blank=True)
    skill_level = models.IntegerField(default=1)
    experience_points = models.IntegerField(default=0)
    reward_points = models.IntegerField(default=0)
    
    def add_experience(self, points):
        # Adds XP and calculates if the user leveled up.
        self.experience_points += points
        
        # Calculate the users level based on their new total XP
        new_level = 1
        while self.experience_points >= (new_level * 50 * (new_level + 1)):
            new_level += 1
            
        # Check if they leveled up
        leveled_up = False
        if new_level > self.skill_level:
            self.skill_level = new_level
            leveled_up = True
            
        self.save()
        # Returns True if user leveled up
        return leveled_up 

    def __str__(self):
        return self.name
    
    # Tells django how to display in admin panel (removes extra s)
    class Meta:
        verbose_name = "User Stats"
        verbose_name_plural = "User Stats"


# Auto-create UserStats when a User signs up
@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance, name=instance.username)

@receiver(post_save, sender=User)
def save_user_stats(sender, instance, **kwargs):
    instance.userstats.save()


# --------------- CHORE MODELS ---------------
class Chore(models.Model):
    # Attributes
    category = models.CharField(max_length=50)
    chore_name = models.CharField(max_length=200)
    frequency = models.CharField(max_length=50)
    difficulty = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    default_points = models.IntegerField()
    
    def __str__(self):
        return self.chore_name


class AssignedChore(models.Model):
    # Attributes
    chore_definition = models.ForeignKey(Chore, on_delete=models.CASCADE)
    # Assign tasks by User account
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    date_assigned = models.DateTimeField(auto_now_add=True)
    date_due = models.DateTimeField(null=True, blank=True)
    # Default points for this chore
    points_value = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.chore_definition.chore_name} - Assigned to {self.assigned_to.username if self.assigned_to else 'Unassigned'}"
    
    def save(self, *args, **kwargs):
        # If points_value is not set manually, grab it from the default
        if self.points_value is None:
            self.points_value = self.chore_definition.default_points
        super().save(*args, **kwargs)


# ------------- Auto-populate chore table -------------
@receiver(post_migrate)
def populate_chores(sender, **kwargs):
    if sender.name == "main": 
        
        # Prevent duplicates if data exists
        if Chore.objects.exists():
            return  

        # Find the path to chores.csv relative to this models.py file
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "chores.csv")

        print(f"Looking for chores CSV at: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                chores_to_create = []
                
                print("Reading CSV and creating chores...")
                
                for row in reader:
                    # Pull values from the new CSV format
                    points = int(row["Default Points"])
                    diff = int(row["Difficulty"])
                    
                    chores_to_create.append(Chore(
                        category=row["Category"],
                        chore_name=row["Chore Name"],
                        frequency=row["Frequency"],
                        difficulty=diff,
                        default_points=points
                    ))
                
                Chore.objects.bulk_create(chores_to_create)
                print(f"Successfully created {len(chores_to_create)} chores.")
                
        except FileNotFoundError:
            print("WARNING: 'chores.csv' not found. Skipping auto-population.")
        except KeyError as e:
            print(f"CSV ERROR: Column {e} not found. Check your CSV headers match the model script.")
        except Exception as e:
            print(f"Error importing chores: {e}")

# ------------- Chore Extention Request -------------
class ChoreExtensionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending',),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    assigned_chore = models.ForeignKey(AssignedChore, on_delete=models.CASCADE, related_name='extension_requests')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)
    requested_due_date = models.DateTimeField(null=True, blank=True)  # Specific date/time user is requesting
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_extensions')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Extension for {self.assigned_chore} by {self.requested_by.username}"