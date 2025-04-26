from django.shortcuts import render, redirect
from .models import HealthCard, Vote, Session
from .forms import VoteForm
from django.contrib.auth.decorators import login_required

# Create your views here.

#@login_required
def vote_view(request):
    session = Session.objects.first()
    cards = HealthCard.objects.all()

    if request.method == 'POST':
        for card in cards:
            vote_value = request.POST.get(f'vote_{card.id}')
            progress = request.POST.get(f'progress_{card.id}') == 'on'

            Vote.objects.update_or_create(
                user=request.user,
                session=session,
                card=card,
                defaults={'vote': vote_value, 'progress': progress}
            )
        
        return redirect('vote')
    return render(request, 'main/vote.html', {'cards': cards})
