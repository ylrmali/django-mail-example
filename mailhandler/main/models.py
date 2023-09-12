from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from utils.models.models import BaseModel
import random
import datetime

# Create your models here.

class CustomUser(AbstractUser):
    is_confirmed = models.BooleanField(default=False)
    access_code = models.CharField(max_length=6, blank=True, null=True)
    code_created = models.DateTimeField(blank=True, null=True)



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'
        unique_together = ['username', 'email']

    def __str__(self):
        return self.username
    
    def set_access_code(self):
        '''
            create 6 digit random access code and set it to access_code
        '''
        code = random.randint(100000, 999999)
        self.access_code = code
        return self
    

    def access_code_expired(self):
        '''
            Check if the access code has expired
        '''
        now = timezone.now()
        if ( now - self.code_created ) > datetime.timedelta(minutes=5):
            return True
        else:
            return False

    
    