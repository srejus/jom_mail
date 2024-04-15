from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from voice_email.utils import create_stripe_payment_link


# Create your views here.

class LoginView(View):
    def get(self,request):
        err = request.GET.get("err")
        type_ = request.GET.get("type_","User")
        return render(request,'login.html',{'err':err,'type_':type_})

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username, " > ",password)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.GET.get("next")
            if next:
                return redirect(next)
            
            acc = Account.objects.get(user=request.user)
            if acc.user_type == 'GOV_EMPLOYEE':
                return redirect("/employee/")
            
            return redirect("/")
        err = "Invalid credentails!"
        return redirect(f"/accounts/login/?err={err}")
    

class SignupView(View):
    def get(self,request):
        err = request.GET.get("err")
        return render(request,'signup.html',{'err':err})
    
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        api_key = request.POST.get("api_key")
        
        if password != password1:
            err = "Password not matching!"
            return redirect(f"/accounts/signup?err={err}")
    
        user = User.objects.filter(username=username)
        if user.exists():
            err = "User with this username already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        acc = Account.objects.filter(email=email).exists()
        if acc:
            err = "User with this email already exists"
            return redirect(f"/accounts/signup?err={err}")
        
        user = User.objects.create_user(username=username,email=email,password=password)
        acc = Account.objects.create(user=user,full_name=full_name)

        return render(request,'org_save.html',{'acc':acc.id})
        

class CreateOrgView(View):
    def get(self,request):
        return render(request,'org_save.html')
    
    def post(self,request):
        org_name = request.POST.get("org_name")
        open_ai_key = request.POST.get("open_ai_apikey")
        supersent_api_key = request.POST.get("supersent_api")
        acc_id = request.POST.get("acc")
        
        acc = Account.objects.get(id=acc_id)
        acc.api_key = supersent_api_key
        acc.org_name = org_name
        acc.open_ai_api = open_ai_key
        acc.save()

        return redirect("/accounts/login/")
    

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("/")
   

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        return render(request,'profile.html',{'acc':acc})
    

@method_decorator(login_required,name='dispatch')
class EditProfileView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        return render(request,'edit_profile.html',{'acc':acc})
    
    def post(self,request):
        acc = Account.objects.get(user=request.user)

        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        org_name = request.POST.get('org_name')
        api_key = request.POST.get('api_key')
        open_ai_api = request.POST.get('open_ai_api')

        acc.phone = phone
        acc.email = email
        acc.address = address
        acc.api_key = api_key
        acc.open_ai_api = open_ai_api
        acc.org_name = org_name

        acc.save()
        return redirect("/accounts/profile")
    

@method_decorator(login_required,name='dispatch')
class RechargeWalletView(View):
    def get(self,request):
        return render(request,"recharge.html")
    
    def post(self,request):
        amount = request.POST.get("amount")
        print("Amount : ",amount)
        pay_url = create_stripe_payment_link(amount)
        print("pay_url : ",pay_url)
        return redirect(pay_url)


@method_decorator(login_required,name='dispatch')
class SuccessView(View):
    def get(self,request):
        acc = Account.objects.get(user=request.user)
        acc.wallet += float(request.GET.get("amt"))
        acc.save()
        return redirect("/accounts/profile")