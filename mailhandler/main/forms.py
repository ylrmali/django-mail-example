from django.forms import ModelForm
from django import forms
from main.models import CustomUser

class RegisterUserForm(ModelForm):
    '''
        user registration form
    '''
    re_password = forms.CharField(max_length=128, widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            're_password': 'Re-Password',
        }
        help_texts = {
            'username': 'Enter your username',
            'email': 'Enter your email',
            'password': 'Enter your password',
            're_password': 'Enter your password again',
        }
        error_messages = {
            'username': {
                'required': 'Please enter your username',
            },
            'email': {
                'required': 'Please enter your email',
            },
            'password': {
                'required': 'Please enter your password',
            },
            're_password': {
                'required': 'Please enter your password again',
            },
        }
       

class LoginUserForm(ModelForm):
    '''
        user login form
    '''

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Username',
            'password': 'Password',
        }
        help_texts = {
            'username': 'Enter your username',
            'password': 'Enter your password',
        }
        error_messages = {
            'username': {
                'required': 'Please enter your username',
            },
            'password': {
                'required': 'Please enter your password',
            },
        }
