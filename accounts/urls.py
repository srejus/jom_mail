from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('signup',SignupView.as_view()),
    path('logout',LogoutView.as_view()),
    path('create-org',CreateOrgView.as_view()),
]