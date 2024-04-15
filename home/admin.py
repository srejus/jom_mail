from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Contact)
admin.site.register(Campaign)
admin.site.register(CampaignContacts)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','phone','email','message']


admin.site.register(IndexContact,ContactAdmin)

