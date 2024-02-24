from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *

# Create your views here.

class LoginView(View):
    def get(self,request):
        err = request.GET.get("err")
        type_ = request.GET.get("type_","User")
        return render(request,'login.html',{'err':err,'type_':type_})

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        
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
        # pincode = request.POST.get("pincode")
        # state = request.POST.get("state")
        # country = request.POST.get("country")
        # address = request.POST.get("address")
        # user_type = request.POST.get("user_type")
        
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
        acc = Account.objects.create(user=user,full_name=full_name,
                                     api_key=api_key)

        return redirect('/accounts/login')
        
    

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("/")