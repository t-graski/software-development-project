from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.user_logout, name='logout'),
    path('progress/', views.UserProgressView.as_view(), name='user_progress'),  # Added 
    #Vote page doesn't work with bellow path active, causes exception, commented it out in case if someone needs it
    #path('vote/<int:check_id>/', views.SubmitVoteView.as_view(), name='submit_vote'), 
    path('logout', views.user_logout, name='logout'),
    path('vote/<int:check_id>/', views.voteView, name='vote'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/engineer', views.engineer_dashboard, name='engineer_dashboard'),
    path('dashboard/teamlead', views.team_leader_dashboard, name='team_leader_dashboard'),
]
