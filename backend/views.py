from django.shortcuts import render
from .models import Session, HealthCard, Vote
from django.contrib.auth.decorators import login_required

@login_required
def user_progress_view(request):
    """
    View to display a logged-in user's voting progress on squad health cards.
    Users can filter by session and health card, and view progress over time
    via a color-coded (traffic light) bar chart, following the Spotify Health Check model.
    """

    # Fetch all available sessions and health cards to populate dropdown filters
    sessions = Session.objects.all()
    health_cards = HealthCard.objects.all()

    # Get selected filters from GET request
    selected_session_id = request.GET.get('session')
    selected_card_id = request.GET.get('card')

    # Initialize vote and chart data containers
    votes = []
    chart_data = []

    # Filter vote list by both session and health card (for vote display under dropdown)
    if selected_session_id and selected_card_id:
        votes = Vote.objects.filter(
            user=request.user,
            session_id=selected_session_id,
            health_card_id=selected_card_id
        )

    # Prepare chart data: all votes for selected health card, ordered by session date
    if selected_card_id:
        progress_votes = Vote.objects.filter(
            user=request.user,
            health_card_id=selected_card_id
        ).order_by('session__date')

        # Format votes for Chart.js: lowercase values to ensure correct color mapping
        chart_data = [
            {
                'session': vote.session.name,
                'vote': vote.vote.lower(),           # Required for JavaScript color logic
                'progress': str(vote.progress).lower()  # Convert boolean to 'true'/'false'
            }
            for vote in progress_votes
        ]

    # Pass all relevant data to the template
    context = {
        'sessions': sessions,
        'health_cards': health_cards,
        'votes': votes,
        'chart_data': chart_data,
    }

    # Render the progress page with chart and vote list
    return render(request, 'user_progress.html', context)
