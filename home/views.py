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
        msg = request.GET.get("msg")
        return render(request,'index.html',{'msg':msg})
    
    def post(self,request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        IndexContact.objects.create(name=name,email=email,phone=phone,message=message)
        msg = "Form Submitted Successfully!"
        return redirect(f"/?msg={msg}")
    

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self,request):
        emails = History.objects.all()
        total_emails = emails.count()
        total_camp = Campaign.objects.all().count()
        wallet = Account.objects.get(user=request.user).wallet
        total_read = emails.filter(total_opened__gt=0).count()
        
        campaigns = Campaign.objects.filter(user__user=request.user)
        return render(request,'dashboard.html',{'campaigns':campaigns,
                                                'total_emails':total_emails,'camp':total_camp,
                                                'wallet':wallet,'read':total_read})
    

@method_decorator(login_required,name='dispatch')
class ContactView(View):
    def get(self,request):
        campaigns = Campaign.objects.filter(user__user=request.user)
        contacts = Contact.objects.filter(user__user=request.user)
        return render(request,'contacts.html',{'contacts':contacts,'campaigns':campaigns})
    

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


import pandas as pd  
from mail.models import History
import requests
from django.conf import settings

@method_decorator(login_required,name='dispatch')
class UploadView(View):
    def get(self,request):
        err = request.GET.get("err")
        return render(request,'upload.html',{'err':err})
    
    def post(self, request):
        file = request.FILES.get("file")
        acc = Account.objects.get(user=request.user)
        
        # Check if a file was uploaded
        if file is not None:
            # Read the CSV file into a DataFrame using pandas
            try:
                df = pd.read_csv(file)
            except pd.errors.EmptyDataError:
                err = "Uploaded file is Empty"
                return redirect(f"/upload?err={err}")
            except pd.errors.ParserError:
                err = "Error parsing the CSV file"
                return redirect(f"/upload?err={err}")
            
            # Loop through each row and print the fields
            for index, row in df.iterrows():
                to = row['to']
                subject = row['subject']
                content = row['content']
                
                print("To:", to)
                print("Subject:", subject)
                print("Content:", content)
                print("\n")

                # sending email
                history = History.objects.create(user=request.user,subject=subject,content=content,to_email=to)
                data = {
                    "subject":subject,
                    "to_email":to,
                    "context":{
                        "message":content
                    },
                    "api_key":acc.api_key,
                    "identifier":str(history.id)
                }
                
                res = requests.post(url=settings.SUPERSENT_URL,headers={},json=data)
                print("res -> ",res.json())

            
            # Redirect to dashboard after processing
            return redirect("/dashboard")
        else:
            err = "No file Uploaded"
            return redirect(f"/upload?err={err}")



class TemplateView(View):
    def get(self,request):
        return render(request,'templates.html')