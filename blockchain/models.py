from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from blockchain.manager import UserManager
from rest_framework.authtoken.models import Token

from django.db.models.signals import post_save
from django.dispatch import receiver
from blockchain_server import settings
# Create your models here.

class blockchain(models.Model):
    Hash                            = models.CharField(max_length = 64, primary_key = True, null = False)
    PreviousHash                    = models.CharField(max_length = 64, null = False)
    TimeStamp                       = models.DateTimeField(null = False)
    BlockData                       = models.TextField(null = False)

class User(AbstractBaseUser):
    username                        = models.CharField(verbose_name = 'username', max_length=30, blank = False, null = False, primary_key = True, unique = True)
    email                           = models.EmailField(verbose_name = 'email', blank = False, null = False, unique = True)

    first_name                      = models.CharField(max_length = 25, blank = False, null = False)
    last_name                       = models.CharField(max_length = 25, blank = False, null = False)
    date_of_birth                   = models.DateField(blank = False, null = False, default = timezone.now)
    
    date_joined                     = models.DateTimeField(verbose_name = 'date_joined', auto_now_add = True)
    last_login                      = models.DateTimeField(verbose_name = 'last_login', auto_now = True) 
    is_staff                        = models.BooleanField(default = False)
    is_admin                        = models.BooleanField(default = False)
    is_active                       = models.BooleanField(default = True)
    is_superuser                    = models.BooleanField(default = False)

    EMAIL_FIELD                     = 'email'
    USERNAME_FIELD                  = 'username'
    REQUIRED_FIELDS                 = ['email', 'first_name', 'last_name', 'date_of_birth']

    objects                         = UserManager()
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)