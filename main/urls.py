from django.urls import path
from . import views

urlpatterns = [
    path('plan-journey/', views.api_plan_journey, name='api_plan_journey'),
]