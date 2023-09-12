from django.contrib.auth import get_user_model
from main.models import CustomUser
from django.utils import timezone
from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponse

def access_code_check(ac):
    '''
    check user's access code is time expired or not
    ac = access code
    '''
    try :
        access_code = CustomUser.objects.get(access_code=ac)
        if access_code:
            if access_code.access_code_expired():
                access_code.delete()
                return False
            else:
                return True
        else:
            return False
    except Exception as e:
        return HttpResponse('whaaat')
    
   


