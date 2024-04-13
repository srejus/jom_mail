import requests

from django.shortcuts import render,redirect
from django.views import View
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import History
from accounts.models import Account
from home.models import *

# Create your views here.
@method_decorator(login_required, name='dispatch')
class CreateNewMail(View):
    def post(self,request):
        subject = request.POST.get("subject")
        to_email = request.POST.get("to")
        campaigns = request.POST.get("campaigns",'0')
        content = request.POST.get("content")
        
        acc = Account.objects.get(user=request.user)
        if acc.wallet < 2:
            msg = "Insufficient Wallet Balance!"
            return redirect(f"/?msg={msg}")
        
        acc.wallet = acc.wallet - 2
        acc.save()

        print("Campaigns : ",campaigns)

        if not to_email and campaigns == '0':
            print("--------Redirecting due to no campaigns and no email--------")
            return redirect("/mail/sent")
        if campaigns != '0':
            campaigns = CampaignContacts.objects.filter(campaign__id=campaigns)
            for c in campaigns:
                to_email = c.contact.email
                history = History.objects.create(user=request.user,subject=subject,content=content,to_email=to_email)
                data = {
                    "subject":subject,
                    "to_email":to_email,
                    "context":{
                        "message":content
                    },
                    "api_key":acc.api_key,
                    "identifier":str(history.id)
                }
                
                res = requests.post(url=settings.SUPERSENT_URL,headers={},json=data)
            
            print("--------Redirecting due to campaigns end--------")
            return redirect("/mail/sent")

        history = History.objects.create(user=request.user,subject=subject,content=content,to_email=to_email)
        data = {
            "subject":subject,
            "to_email":to_email,
            "context":{
                "message":content
            },
            "api_key":acc.api_key,
            "identifier":str(history.id)
        }
        
        res = requests.post(url=settings.SUPERSENT_URL,headers={},json=data)
        print("res -> ",res.json())

        return redirect("/mail/sent")
    

from home.utils import update_read_status

@method_decorator(login_required, name='dispatch')
class SentMailView(View):
    def get(self,request):
        type_ = request.GET.get("type_")
        if type_ == 'star':
            emails = History.objects.filter(user=request.user,is_stared=True)
            return render(request,'star.html',{'emails':emails})
        elif type_ == 'draft':
            emails = History.objects.filter(user=request.user,status='DRAFT')
            return render(request,'draft.html',{'emails':emails})
        
        emails = History.objects.filter(user=request.user,status__in=['SENT','READ']).order_by('-id')
        
        # call read api to update status
        acc = Account.objects.get(user=request.user)
        update_read_status(acc)
        return render(request,"sent.html",{'emails':emails})
    

@method_decorator(login_required, name='dispatch')
class ReadMailView(View):
    def get(self,request,id):
        email = History.objects.get(id=id)
        return render(request,'read_mail.html',{'email':email})