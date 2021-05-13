from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model): 
    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    name                = models.CharField(max_length=30, default="forgot")
    codeForces_username = models.CharField(max_length=30)
    year                = models.IntegerField(help_text='Year of Admission')
    
    def __str__(self):
        return "{}".format(self.codeForces_username)
    
    @classmethod
    def create(cls,*args, **kwargs):
        profile=UserProfile(
            
        )
        return profile