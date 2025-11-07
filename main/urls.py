# main/urls.py (This is your NEW file)

from django.urls import path
from . import views  # Import views from this app

urlpatterns = [
    # This creates the URL: /api/plan-journey/
    # When JavaScript sends data here, it will run the
    # 'api_plan_journey' view function.
    path('plan-journey/', views.api_plan_journey, name='api_plan_journey'),
]