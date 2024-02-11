from django.urls import path
from . views import *

urlpatterns = [
    path('<int:id>',ReadMailView.as_view()),
    path('new-email/',CreateNewMail.as_view()),
    path('sent',SentMailView.as_view()),
]