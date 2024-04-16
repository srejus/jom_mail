from django.urls import path
from . views import *

urlpatterns = [
    path('',IndexView.as_view()),
    path('dashboard',DashboardView.as_view(),name='da'),
    path('dashboard/',DashboardView.as_view(),name='das'),
    path('contacts',ContactView.as_view()),
    path('contacts/delete/<int:id>',DeleteContactView.as_view()),
    path('contacts/add',AddContactView.as_view()),

    path('campaign',CampaignView.as_view()),
    path('campaign/add',AddCampaignView.as_view()),
    path('campaign/delete/<int:id>',DeleteCampaignView.as_view()),

    path('rewrite',RewriteView.as_view()),

    path('upload',UploadView.as_view()),

    path('templates',TemplateView.as_view()),

    path('register',RegisterOrgView.as_view()),
]