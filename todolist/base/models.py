from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile',unique=True,null=True,blank=True)
    phone_number=models.CharField(max_length=13,null=True,blank=True)
    otp=models.IntegerField(null=True,blank=True)
    uid=models.UUIDField(default=uuid.uuid4)


class task(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,unique=True,null=True,blank=True)
    title=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    complete=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['complete']