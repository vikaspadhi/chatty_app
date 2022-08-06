import email
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.
class User(AbstractUser):
    username=None
    mobile = models.CharField(max_length=10,unique=True)
    objects=UserManager()
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.mobile