from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('profile', views.profile, name='profile'),
    path('logout', views.user_logout, name='logout'),
    path('team-summary/', views.team_summary_view, name='team_summary'),
]
