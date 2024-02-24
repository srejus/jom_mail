from django.urls import path
from . views import *

urlpatterns = [
    path('',IndexView.as_view()),
    path('dashboard',DashboardView.as_view())
]