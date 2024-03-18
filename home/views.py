from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import *
from accounts.models import Account


# Create your views here.
class IndexView(View):
    def get(self,request):
        return render(request,'index.html')
    

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self,request):
        campaigns = Campaign.objects.filter(user__user=request.user)
        return render(request,'dashboard.html',{'campaigns':campaigns})
    

@method_decorator(login_required,name='dispatch')
class ContactView(View):
    def get(self,request):
        contacts = Contact.objects.filter(user__user=request.user)
        return render(request,'contacts.html',{'contacts':contacts})
    

@method_decorator(login_required,name='dispatch')
class DeleteContactView(View):
    def get(self,request,id):
        Contact.objects.filter(id=id).delete()
        return redirect("/contacts")


@method_decorator(login_required,name='dispatch')
class AddContactView(View):
    def get(self,request):
        return render(request,'add_contact.html')
    
    def post(self,request):
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")

        acc = Account.objects.get(user=request.user)
        Contact.objects.create(user=acc,full_name=full_name,email=email)
        return redirect("/contacts")
    

@method_decorator(login_required,name='dispatch')
class CampaignView(View):
    def get(self,request):
        campaigns = Campaign.objects.filter(user__user=request.user)
        return render(request,'camp.html',{'campaigns':campaigns})


@method_decorator(login_required,name='dispatch')
class DeleteCampaignView(View):
    def get(self,request,id):
        Campaign.objects.filter(id=id).delete()
        return redirect("/campaign")


@method_decorator(login_required,name='dispatch')
class AddCampaignView(View):
    def get(self,request):
        contacts = Contact.objects.filter(user__user=request.user)
        return render(request,'camp_add.html',{'contacts':contacts})
    
    def post(self,request):
        name = request.POST.get("name")
        contacts = request.POST.getlist("contact")

        acc = Account.objects.get(user=request.user)
        campaign = Campaign.objects.create(user=acc,name=name)
        for i in contacts:
            contact = Contact.objects.get(id=i)
            CampaignContacts.objects.create(campaign=campaign,contact=contact)
        return redirect("/campaign")



@method_decorator(csrf_exempt, name='dispatch')
class RewriteView(View):
    def post(self,request):
        content = request.GET.get("content")
        return JsonResponse({"message":"New Content"})