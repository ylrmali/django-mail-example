from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage, EmailMultiAlternatives
from main.forms import RegisterUserForm, LoginUserForm
from main.models import CustomUser
from utils.auth.mail import MailHandler as Mail
from utils.auth.access_code_check import access_code_check
from django.contrib.auth import login, logout, authenticate
import random

# Create your views here.
def eMail(request):
    if request.method == 'POST':
         with get_connection(  
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS  
       ) as connection:  
            EmailMessage(
                subject='Mail from django backend',
                body='test mail from django backend with EmailMessage',
                from_email='ylrmali1289@gmail.com',
                to=['ali.yildirim@norbit.com.tr'],
                reply_to=False,
                connection=connection,
            ).send()

    return render(request, 'main/index.html')


def index(request):
    return render(request, 'main/index.html')

from django.core.mail import EmailMessage, get_connection
from django.conf import settings

def send_email(request):  
   if request.method == "POST": 
       with get_connection(  
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS  
       ) as connection:  
           subject = 'Test email'
           email_from = settings.EMAIL_HOST_USER  
           recipient_list = ['ali.yildirim@norbit.com.tr', ]  
           message = 'This is a test email.'  
        #    mail = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
           html_content = "<p>This is an <strong>important</strong> message.</p>"
           msg = EmailMultiAlternatives(subject, message, email_from, recipient_list, connection=connection)
           msg.attach_alternative(html_content, "text/html")
           msg.attach_file('/home/ali/project/django-email/mailhandler/main/static/main/img/test.txt') # attach a file
           msg.send()
        #    mail.send()
 
   return render(request, 'main/index.html')

def custom_login(request):
    form = LoginUserForm()
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            try:
                user = authenticate(username=username, password=password)
                if user is not None and user.is_confirmed:
                    login(request, user)
                    return HttpResponse('You have successfully logged in!')
                else:
                    return HttpResponse('Please confirm your email address!')
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse('Please fill in all fields!')
    return render(request, 'main/login.html', context={'form': form})


def confirm(request):
    '''
        confirm user access code
    '''
    if request.method == 'POST':
        access_code = request.POST.get('access_code')
        if access_code:
            try:
                condition = access_code_check(access_code)
                if condition:
                    user = CustomUser.objects.get(access_code=access_code)
                    user.is_confirmed = True
                    user.save()
                    # after confirm delete access code
                    user.access_code = None
                    user.code_created = None
                    return HttpResponse(' \
                                    You have successfully confirmed your email address! <br> \
                                    <a href="/login/">Login</a> \
                                    ')
                else:
                    return HttpResponse('Your access code has expired. Please get new access code.\
                                    <a href="/confirm/">Get new access code</a>')
            except CustomUser.DoesNotExist as e:
                return HttpResponse(e)
        else:
            return HttpResponse('Please enter your access code!')
        
    return render(request, 'main/confirm.html')

def register(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('re_password')

        if username and email and password1 and password2:
            if password1 == password2:
                try:
                    # random access code
                    user = CustomUser.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    return HttpResponse(' \
                                        You have successfully registered <br> \
                                        Please check your email and enter the access code.<br>  \
                                        <a href="/confirm/">Confirm Account</a> \
                                        ')
                except Exception as e:
                    return HttpResponse(e)

            else:
                return HttpResponse('Passwords do not match!')
        else:
            return HttpResponse('Please fill in all fields!')

        

    return render(request, 'main/register.html', context={'form': form})