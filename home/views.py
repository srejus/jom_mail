from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class IndexView(View):
    def get(self,request):
        return render(request,'index.html')
    

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self,request):
        return render(request,'dashboard.html')