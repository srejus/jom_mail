from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    USER_TYPE_CHOICES = (
        ('USER','USER'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    full_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    user_type = models.CharField(max_length=100,default='USER',choices=USER_TYPE_CHOICES)
    address = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    pincode = models.CharField(max_length=6,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    wallet = models.FloatField(default=0.0)

    org_name = models.CharField(max_length=100,null=True,blank=True)
    api_key  = models.CharField(max_length=200,null=True,blank=True)
    open_ai_api = models.CharField(max_length=200,null=True,blank=True)
    
    def __str__(self):
        return str(self.full_name)
    

class Organization(models.Model):
    STATUS_CHOICES = (
        ('created','created'),
        ('accepted','accepted'),
        ('rejected','rejected'),
    )

    org_name = models.CharField(max_length=100)
    email_id = models.EmailField(null=True,blank=True)
    org_address = models.CharField(max_length=150,null=True,blank=True)
    approve_status = models.CharField(max_length=100,default='created',choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)