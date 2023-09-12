from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from main.models import CustomUser
from utils.auth.mail import MailHandler as Mail
from django.http import HttpResponse
import random
from django.utils import timezone 

@receiver(post_save, sender=CustomUser)
def create_access_code(sender, instance, created, **kwargs):
    '''
        create access token when user created
    '''
    if created:
        try:
            #? get user information
            username = instance.username
            email = instance.email

            #? create access code
            random_code = random.randint(100000, 999999)
            instance.access_code = random_code
            instance.code_created = timezone.now()
            print('Access code created')


            #? after created access code send email to user
            Mail().send_html(
                subject='Django Test Register',
                message='You have successfully registered',
                recipient_list=[email, ],
                username=username,
                access_code=random_code,
            )
           
        except Exception as e:
            return HttpResponse(e)



