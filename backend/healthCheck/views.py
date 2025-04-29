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

@login_required
def voteView(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return HttpResponse("You don't have an Employee profile yet. Please contact an administrator")
    
    team = employee.teamId    

    cards = HealthCheckType.objects.all()
    print(f"Cards: {cards}")

    if request.method == 'POST':
        print(request.POST)

        if 'save' in request.POST:           
            return redirect('vote')

        else:
            healthCheck = HealthCheck.objects.create(
            employeeId = employee,
            teamId = team
        )   

        for card in cards:
            voteValue = request.POST.get(f'vote_{card.typeId}')
            progressValue = request.POST.get(f'progress_{card.typeId}')

            print(f"Vote value for {card.typeId}: {voteValue}")
            print(f"Direction value for {card.typeId}: {progressValue}")

            if voteValue and progressValue:
                HealthCheckVotes.objects.update_or_create(
                    checkId = healthCheck,
                    typeId = card,
                    defaults = {'vote': voteValue, 'direction': progressValue}
                )
            else:
                print(f"No vote selected for card {card.typeId}")
        
        return redirect('vote')

    return render(request, 'healthChecks/vote.html', {'cards': cards})
