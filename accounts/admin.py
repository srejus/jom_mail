from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Account)

class OrgAdmin(admin.ModelAdmin):
    list_display = ['org_name','email_id','approve_status']


admin.site.register(Organization,OrgAdmin)