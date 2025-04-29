from datetime import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader

from healthCheck.forms import RegisterForm, LoginForm
from healthCheck.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from .decorators import role_required
from .models import Employee, HealthCheck, HealthCheckVotes, HealthCheckType
from django.contrib import messages


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
def profile(request):
    user = request.user
    employee = user.employee

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        team_id = request.POST['team']

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        employee.teamId = Team.objects.get(pk=team_id)
        employee.save()

        return redirect('profile')

    all_teams = Team.objects.all()

    return render(request, 'healthChecks/profile.html', {'teams': all_teams})


def user_logout(request):
    logout(request)
    return redirect('login')


@method_decorator(login_required, name='dispatch')
class UserProgressView(View):
    def get(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            messages.error(request, 'Employee profile not found.')
            return redirect('profile')  # Or some safe fallback

        sessions = HealthCheck.objects.filter(employeeId=employee)
        selected_session_id = request.GET.get('session_id')

        votes = HealthCheckVotes.objects.none()
        if selected_session_id:
            votes = HealthCheckVotes.objects.filter(
                checkId__checkId=selected_session_id,
                checkId__employeeId=employee
            )

        types = HealthCheckType.objects.all()
        vote_data = {type_.displayName: 0 for type_ in types}

        for vote in votes:
            vote_data[vote.typeId.displayName] += 1

        context = {
            'sessions': sessions,
            'selected_session_id': int(selected_session_id) if selected_session_id else None,
            'vote_data': vote_data,
        }
        return render(request, 'healthChecks/user_progress.html', context)


@method_decorator(login_required, name='dispatch')
class SubmitVoteView(View):
    def post(self, request, check_id):
        try:
            employee = Employee.objects.get(email=request.user.email)
        except Employee.DoesNotExist:
            messages.error(request, 'Employee profile not found.')
            return redirect('user_progress')

        healthcheck = get_object_or_404(HealthCheck, checkId=check_id)

        vote_value = request.POST.get('vote')
        type_id = request.POST.get('type_id')
        direction = request.POST.get('direction')

        if not vote_value or not type_id or not direction:
            messages.error(request, 'All fields are required.')
            return redirect('user_progress')

        already_voted = HealthCheckVotes.objects.filter(
            checkId=healthcheck,
            typeId_id=type_id
        ).exists()

        if already_voted:
            messages.warning(request, 'Already voted for this check and type.')
        else:
            HealthCheckVotes.objects.create(
                checkId=healthcheck,
                typeId_id=type_id,
                vote=vote_value,
                direction=direction,
            )
            messages.success(request, 'Vote recorded successfully.')

        return redirect('user_progress')


@login_required
def voteView(request, check_id=None):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        return HttpResponse("You don't have an Employee profile yet. Please contact an administrator")

    existingVotes = {}
    healthCheck = None

    if check_id:
        healthCheck = get_object_or_404(HealthCheck, checkId=check_id)

        for vote in HealthCheckVotes.objects.filter(checkId=healthCheck):
            existingVotes[vote.typeId.typeId] = {'vote': vote.vote, 'direction': vote.direction}

        print(f"Exisitng votes: {existingVotes}")

    team = employee.teamId
    cards = HealthCheckType.objects.all()

    for card in cards:
        voteData = existingVotes.get(card.typeId)
        card.vote = voteData['vote'] if voteData else None
        card.direction = voteData['direction'] if voteData else None

        print(f"Card {card.typeId} - Vote: {card.vote}, Direction: {card.direction}")

    print(f"Cards: {cards}")

    if request.method == 'POST':
        print(request.POST)

        isSubmit = 'submit' in request.POST
        isSave = 'save' in request.POST

        if not healthCheck:
            healthCheck = HealthCheck.objects.create(
                employeeId=employee,
                teamId=team,
                hasCompleted=isSubmit,
                hasStarted=True
            )

        if isSubmit:
            healthCheck.hasCompleted = True
            healthCheck.save()

        if isSave:
            healthCheck.hasStarted = True
            healthCheck.save()

        for card in cards:
            voteValue = request.POST.get(f'vote_{card.typeId}')
            progressValue = request.POST.get(f'progress_{card.typeId}')

            print(f"Vote value for {card.typeId}: {voteValue}")
            print(f"Direction value for {card.typeId}: {progressValue}")

            if voteValue and progressValue:
                HealthCheckVotes.objects.update_or_create(
                    checkId=healthCheck,
                    typeId=card,
                    defaults={'vote': voteValue, 'direction': progressValue}
                )
            else:
                print(f"No vote or progress selected for card {card.typeId}")

        return redirect('dashboard')

    return render(request, 'healthChecks/vote.html', {'cards': cards, 'healthCheck': healthCheck})


@login_required
def dashboard(request):
    role = request.user.employee.roleType
    if role == 'engineer':
        return redirect('engineer_dashboard')
    elif role == 'teamlead':
        return redirect('team_leader_dashboard')
    elif role == 'deptlead':
        return redirect('department_leader_dashboard')
    elif role == 'senior':
        return redirect('senior_manager_dashboard')
    return HttpResponseForbidden("Invalid role")


@login_required
@role_required(allowed_roles=['engineer'])
def engineer_dashboard(request):
    employee = request.user.employee
    team_links = EmployeeTeams.objects.filter(employeeId=employee).select_related('teamId')
    teams = [link.teamId for link in team_links]
    selected_team_id = request.GET.get('selected_team_id')

    if selected_team_id:
        sessions = HealthCheck.objects.filter(teamId__teamId=selected_team_id, employeeId=employee)
    else:
        sessions = HealthCheck.objects.filter(employeeId=employee)

    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    context = {
        'sessions': sessions,
        'employee': employee,
        'teams': teams,
        'selected_team_id': selected_team_id,
        'greeting': f"{greeting}, {employee.user.first_name}!"
    }

    return render(request, 'healthChecks/dashboard/engineer.html', context)


@login_required
@role_required(allowed_roles=['teamlead'])
def team_leader_dashboard(request):
    employee = request.user.employee

    lead_teams = Team.objects.filter(
        departmentId__in=Team.objects.filter(
            employeeteams__employeeId=employee
        ).values_list('departmentId', flat=True)
    ).distinct()

    all_cards = HealthCheckType.objects.all()

    selected_team_id = request.GET.get('selected_team_id')
    selected_card_id = request.GET.get('selected_card_id')

    sessions = HealthCheck.objects.filter(teamId__in=lead_teams)

    if selected_team_id:
        sessions = sessions.filter(teamId__teamId=selected_team_id)
    if selected_card_id:
        sessions = sessions.filter(healthcheckvotes__typeId__typeId=selected_card_id)

    context = {
        'teams': lead_teams,
        'cards': all_cards,
        'sessions': sessions,
        'selected_team_id': selected_team_id,
        'selected_card_id': selected_card_id,
    }

    return render(request, 'healthChecks/dashboard/team_leader.html', context)


@login_required
@role_required(allowed_roles=['deptlead'])
def department_leader_dashboard(request):
    employee = request.user.employee

    lead_teams = Team.objects.filter(
        departmentId__in=Team.objects.filter(
            employeeteams__employeeId=employee
        ).values_list('departmentId', flat=True)
    ).distinct()

    all_cards = HealthCheckType.objects.all()

    selected_team_id = request.GET.get('selected_team_id')
    selected_card_id = request.GET.get('selected_card_id')

    sessions = HealthCheck.objects.filter(teamId__in=lead_teams)

    if selected_team_id:
        sessions = sessions.filter(teamId__teamId=selected_team_id)
    if selected_card_id:
        sessions = sessions.filter(healthcheckvotes__typeId__typeId=selected_card_id)

    context = {
        'teams': lead_teams,
        'cards': all_cards,
        'sessions': sessions,
        'selected_team_id': selected_team_id,
        'selected_card_id': selected_card_id,
    }

    return render(request, 'healthChecks/dashboard/department_leader.html', context)


@login_required
@role_required(allowed_roles=['senior'])
def senior_manager_dashboard(request):
    selected_team_id = request.GET.get('selected_team_id')
    teams = Team.objects.all()

    if selected_team_id:
        health_checks = HealthCheck.objects.filter(teamId=selected_team_id)
    else:
        health_checks = HealthCheck.objects.all()

    context = {
        "sessions": health_checks,
        "teams": teams,
        "selected_team_id": selected_team_id,
    }

    return render(request, "healthChecks/dashboard/senior_manager.html", context)
