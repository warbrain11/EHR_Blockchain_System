from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from blockchain.manager import *
from rest_framework.authtoken.models import Token

from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from blockchain_server import settings
import hashlib
# Create your models here.

class blockchain(models.Model):
    Hash                            = models.CharField(max_length = 65, null = True, blank = True)
    PreviousHash                    = models.CharField(max_length = 65, null = True, blank = True)
    TimeStamp                       = models.DateTimeField(null = False)
    BlockData                       = models.TextField(null = False)

    objects                         = Blockchain_Manager()

    class Meta:
        db_table                    = 'Blockchain'

class User(AbstractBaseUser):
    username                        = models.CharField(verbose_name = 'username', max_length=30, blank = False, null = False, primary_key = True, unique = True)
    email                           = models.EmailField(verbose_name = 'email', blank = False, null = False, unique = True)

    verification                    = models.FileField(verbose_name = "verification", upload_to = "uploads/verification", null = True)

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
    REQUIRED_FIELDS                 = ['email', 'first_name', 'last_name', 'date_of_birth', 'verification']

    objects                         = UserManager()
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

#Creates a token for a user each time a user is created
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)

@receiver(pre_save, sender = blockchain)
def update_hash(sender, instance, **kwargs):
    h = hashlib.sha256()
    
    prev_hash = instance.PreviousHash
    time_stamp = datetime.strftime(instance.TimeStamp,  "%Y-%m-%dT%H:%M:%S")
    block_data = instance.BlockData
        
    h.update(bytes(prev_hash, encoding = 'utf-8'))
    h.update(bytes(time_stamp, encoding = 'utf-8'))
    h.update(bytes(block_data, encoding = 'utf-8'))

    my_hash = h.hexdigest()

    instance.Hash = my_hash


"""
@receiver(pre_delete, sender = blockchain)
def prevent_delete(sender, instance, **kwargs):
    raise Exception('Cannot delete a block. Sorry not sorry.')
"""

class Register_Access_Codes(models.Model):
    code                            = models.CharField(max_length = 65, null = True, blank = True)
    email                           = models.CharField(verbose_name = 'email', max_length=30, blank = False, null = True, unique = True)






