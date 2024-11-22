from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import FitnessRecord, User
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import User  # Import the User model or your custom user model
from django.http import Http404



User = get_user_model()  # Use this to reference the custom user model

def home(request):
    return render(request,"index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('handlelogin')
    
    return render(request, 'signup.html')

        
def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('handlelogin')
    
    return render(request, 'handlelogin.html')


def handlelogout(request):
    logout(request)
    messages.success(request,"")    
    return redirect('home')

def personal_training(request):
    return render(request,"personal_training.html")

def physical_therapy(request):
    return render(request,"physical_therapy.html")

def nutrition_council(request):
    return render(request,"nutrition_council.html")

def wellness_program(request):
    return render(request,"wellness_program.html")

def group_classes(request):
    return render(request,"group_classes.html")

def delete_users(request):
    return render(request,"delete_users.html")

def our_vision(request):
    return render(request,"our_vision.html")
# def services(request):
#     return render(request,"services.html")

@login_required(login_url='/login/')
def fitness(request):
     return render(request, "fitness_tracker.html")

# view for bmi calculator
@login_required(login_url='/login/')
def bmi_calculator(request):
    if request.method == 'POST':
            try:
                height = float(request.POST.get('height'))
                weight = float(request.POST.get('weight'))

                if height <= 0 or weight <= 0:
                    messages.error(request, "Height and weight must be positive values.")
                    return redirect('bmi_calculator')

                height_in_meters = height / 100
                bmi = weight / (height_in_meters ** 2)
                category = FitnessRecord.calculate_bmi_category(bmi)

                # Save the fitness record
                FitnessRecord.objects.create(
                    user=request.user,
                    height=height,
                    weight=weight,
                    bmi=bmi,
                    category=category
                )

                return render(request, 'bmi_calculator.html', {
                    'bmi': round(bmi, 2),
                    'category': category,
                    'success': "Your BMI has been calculated and saved successfully!"
                })

            except ValueError:
                messages.error(request, "Please enter valid numerical values for height and weight.")
                return redirect('bmi_calculator')
    return render(request, 'bmi_calculator.html')

@login_required(login_url='/login/')
def fitness_records(request):
    records = FitnessRecord.objects.filter(user=request.user).order_by('-date_recorded')
    return render(request, 'fitness_records.html', {'records': records})

def trainer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_trainer:  # Check if the user is a trainer
                login(request, user)
                return redirect('trainer_dashboard')  # Replace with your trainer dashboard view
            else:
                messages.error(request, "You are not authorized to log in as a trainer.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'trainer_login.html')  # Replace with your trainer login template

@login_required
def trainer_dashboard(request):
    if not request.user.is_trainer:
        return redirect('home')  # If the user is not a trainer, redirect to login page

    # Fetch all fitness records
    records = FitnessRecord.objects.all()  # You can adjust this query based on your needs
    return render(request, 'trainer_dashboard.html', {'records': records})

def trainer_dashboard(request):
    username = request.GET.get('username', '').strip()  # Get the username from the search form
    fitness_records = []
    user = None

    if username:  # Check if a username is provided
        try:
            user = get_object_or_404(User, username=username)  # Fetch the user by username
            fitness_records = FitnessRecord.objects.filter(user=user)  # Filter fitness records for the user
        except User.DoesNotExist:
            user = None  # Handle non-existent username

    context = {
        'fitness_records': fitness_records,
        'user': user,
        'searched_username': username,
    }
    return render(request, 'trainer_dashboard.html', context)


# View to display the user list and allow deletion
def delete_users(request):
    # Fetch all users
    users = User.objects.filter(is_staff=False)

    if request.method == 'POST':
        # Get the username from the POST request to delete the user
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)

        # Delete all fitness records associated with this user
        FitnessRecord.objects.filter(user=user).delete()

        # Delete the user
        user.delete()

        return redirect('delete_users')  # Redirect back to the delete_users page after deletion

    # Render the user list
    return render(request, 'delete_users.html', {'users': users})


