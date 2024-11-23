from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings  # Import settings to refer to the custom User model
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_trainer = models.BooleanField(default=False)  # Flag to indicate if the user is a trainer
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits.")],
        unique=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Trainer(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # You can hash passwords later if needed

    def __str__(self):
        return self.username

class FitnessRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL instead of auth.User
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    category = models.CharField(max_length=50)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fitness Record for {self.user.username} on {self.date_recorded}"

    @staticmethod
    def calculate_bmi_category(bmi):
        """Determine the BMI category."""
        if bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= bmi <= 24.9:
            return 'Normal'
        elif 25 <= bmi <= 29.9:
            return 'Overweight'
        else:
            return 'Obese'
