from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib.auth.models import User

from healthCheck.decorators import role_required
from healthCheck.forms import RegisterForm, LoginForm
from healthCheck.models import Employee
from healthCheck.models import *


# Create your views here.
@login_required
def index(request):
    employees = Employee.objects.all()
    template = loader.get_template("healthChecks/vote.html")
    context = {
        "employees": employees
    }
    return HttpResponse(template.render(context, request))


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']
            )
            Employee.objects.create(
                user=user,
                roleType='engineer'
            )
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'healthChecks/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                user = authenticate(request, username=user.username, password=password)
                if user:
                    login(request, user)
                    return redirect('/')
                else:
                    form.add_error(None, "Invalid credentials.")
            except:
                form.add_error(None, "User does not exist.")
    else:
        form = LoginForm()
    return render(request, 'healthChecks/login.html', {'form': form})


@login_required
@role_required(allowed_roles=['admin'])
def profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        return redirect('profile')
    return render(request, 'healthChecks/profile.html')

def user_logout(request):
    logout(request)
    return redirect('login')

# Author: Soumashik Chatterjee - Implemented user progress tracking and voting logic (views & submission handling)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Employee, HealthCheck, HealthCheckVotes, HealthCheckType
from django.contrib import messages

# View for displaying the user's progress dashboard with vote history
@method_decorator(login_required, name='dispatch')
class UserProgressView(View):
    def get(self, request):
        try:
            # Fetch the current employee profile for the logged-in user
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            # Handle missing profile scenario gracefully
            messages.error(request, 'Employee profile not found.')
            return redirect('profile')  # Fallback route

        # Get all health check sessions for the user
        sessions = HealthCheck.objects.filter(employeeId=employee)

        # Get session ID from the query parameter (if selected)
        selected_session_id = request.GET.get('session_id')

        # Initialize empty vote queryset
        votes = HealthCheckVotes.objects.none()
        if selected_session_id:
            # Filter votes belonging to the selected session and user
            votes = HealthCheckVotes.objects.filter(
                checkId__checkId=selected_session_id,
                checkId__employeeId=employee
            )

        # Initialize vote data structure using all available health check types
        types = HealthCheckType.objects.all()
        vote_data = {type_.displayName: 0 for type_ in types}

        # Aggregate vote counts per category/type
        for vote in votes:
            vote_data[vote.typeId.displayName] += 1

        # Pass all necessary data to the template
        context = {
            'sessions': sessions,
            'selected_session_id': int(selected_session_id) if selected_session_id else None,
            'vote_data': vote_data,
        }
        return render(request, 'healthChecks/user_progress.html', context)

# View to handle vote submission from the user
@method_decorator(login_required, name='dispatch')
class SubmitVoteView(View):
    def post(self, request, check_id):
        try:
            # Find the employee object for the currently logged-in user
            employee = Employee.objects.get(email=request.user.email)
        except Employee.DoesNotExist:
            messages.error(request, 'Employee profile not found.')
            return redirect('user_progress')

        # Get the associated health check instance using the check ID
        healthcheck = get_object_or_404(HealthCheck, checkId=check_id)

        # Extract form values from POST request
        vote_value = request.POST.get('vote')
        type_id = request.POST.get('type_id')
        direction = request.POST.get('direction')

        # Validate that all fields are filled
        if not vote_value or not type_id or not direction:
            messages.error(request, 'All fields are required.')
            return redirect('user_progress')

        # Prevent duplicate votes for the same check and type
        already_voted = HealthCheckVotes.objects.filter(
            checkId=healthcheck,
            typeId_id=type_id
        ).exists()

        if already_voted:
            messages.warning(request, 'Already voted for this check and type.')
        else:
            # Create new vote entry if not already submitted
            HealthCheckVotes.objects.create(
                checkId=healthcheck,
                typeId_id=type_id,
                vote=vote_value,
                direction=direction,
            )
            messages.success(request, 'Vote recorded successfully.')

        return redirect('user_progress')

# View to display the vote cards and allow new vote submissions
@login_required
def voteView(request):
    try:
        # Get the current employee object
        employee = request.user.employee
    except Employee.DoesNotExist:
        return HttpResponse("You don't have an Employee profile yet. Please contact an administrator")
    
    team = employee.teamId  # Get the employee's team

    # Load all health check types to display as cards
    cards = HealthCheckType.objects.all()
    print(f"Cards: {cards}")  # Debugging output

    if request.method == 'POST':
        print(request.POST)  # Debugging form data

        if 'save' in request.POST:
            return redirect('vote')  # Simple save action (future-proofing)

        else:
            # Create a new health check record for the employee
            healthCheck = HealthCheck.objects.create(
                employeeId=employee,
                teamId=team
            )

            # Loop through each card type and retrieve submitted vote and direction
            for card in cards:
                voteValue = request.POST.get(f'vote_{card.typeId}')
                progressValue = request.POST.get(f'progress_{card.typeId}')

                print(f"Vote value for {card.typeId}: {voteValue}")  # Debugging
                print(f"Direction value for {card.typeId}: {progressValue}")  # Debugging

                if voteValue and progressValue:
                    # Create or update the vote entry per card type
                    HealthCheckVotes.objects.update_or_create(
                        checkId=healthCheck,
                        typeId=card,
                        defaults={'vote': voteValue, 'direction': progressValue}
                    )
                else:
                    print(f"No vote selected for card {card.typeId}")  # Incomplete submission log
        
        return redirect('vote')  # Redirect after submission

    return render(request, 'healthChecks/vote.html', {'cards': cards})
