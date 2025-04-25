from django.urls import path
from . import views  # Import views from the current app

# Define URL patterns for the app
urlpatterns = [
    # Route for viewing user voting progress page
    path('user/progress/', views.user_progress_view, name='user_progress'),
]
