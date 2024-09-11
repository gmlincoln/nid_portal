from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Custom_User(AbstractUser):
    
    USER = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('viewer', 'Viewer')
    ]
    
    user_type = models.CharField(choices=USER, max_length=30, null=True)
    profile_pic = models.ImageField(upload_to='Media/Profile_Pic', null=True)


class NID_Model(models.Model):
    
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE, null=True)
    
    nid_number = models.CharField(max_length=100, null=True)
    date_of_issue = models.DateField(max_length=100, null=True)
    place_of_issue = models.CharField(max_length=100, null=True)
    