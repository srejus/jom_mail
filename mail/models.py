from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class History(models.Model):
    SATTUS_CHOICES = (
        ('DRAFT','DRAFT'),
        ('SENT','SENT'),
        ('READ','READ'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='email_send_by')
    subject = models.CharField(max_length=150)
    to_email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_stared = models.BooleanField(default=False)
    total_opened = models.IntegerField(default=0)
    status = models.CharField(max_length=15,default='SENT')
