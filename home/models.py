from django.db import models
from accounts.models import Account


# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='contact_user')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.full_name)+" > "+str(self.email)
    


class Campaign(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='campaign_user')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class CampaignContacts(models.Model):
    campaign = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name='campaign_contact')
    contact = models.ForeignKey(Contact,on_delete=models.CASCADE)




class IndexContact(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    message = models.TextField(null=True,blank=True)