from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.user_logout, name='logout'),	
    path('progress/', views.UserProgressView.as_view(), name='user_progress'),  # Added by Soumashik Chatterjee - Displays user progress dashboard with vote visualization
    path('vote/<int:check_id>/', views.SubmitVoteView.as_view(), name='submit_vote'),  # Added by Soumashik Chatterjee - Handles vote submission for a specific health check
    path('logout', views.user_logout, name='logout'),
    path('vote/', views.voteView, name = 'vote')
]
