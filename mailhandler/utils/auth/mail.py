from django.core.mail import ( 
    EmailMessage,
    EmailMultiAlternatives, 
    get_connection,
)
from django.conf import settings
from django.contrib.auth import get_user_model
import random



class MailHandler:
    '''
    MailHandler class
    '''
    def __init__(self):
        self.__subject = None
        self.__body = None
        self.__from = None
        self.__to = None
        self.__attachment = None
        self.__access_code = None


    def set_subject(self, subject):
        self.__subject = subject
        return self
    
    def set_body(self, body):
        self.__body = body
        return self
    
    def set_from(self, _from):
        self.__from = _from
        return self
    
    def set_to(self, _to):
        self.__to = _to
        return self
    
    def set_attachment(self, attachment):
        self.__attachment = attachment
        return self

    def set_access_code(self, access_code):
        '''
            create 6 digit random access code and set it to access_code
        '''
        self.__access_code = access_code
        return self       
    
    def get_access_code(self):
        return self.__access_code
    
    def get_subject(self):
        return self.__subject
    
    def get_body(self):
        return self.__body
    
    def get_from(self):
        return self.__from
    
    def get_to(self):
        return self.__to
    
    def get_attachment(self):
        return self.__attachment
    
    def send(self):
        '''
            send emails with django.core.mail.EmailMessage
        '''
        with get_connection(  
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS  
        ) as connection:  
            subject = self.get_subject()
            email_from = self.get_from()
            recipient_list = self.get_to()
            message = self.get_body()
            mail = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
            if self.get_attachment() is not None:
                mail.attach_file(self.get_attachment())
            mail.send()
            return True
        return False
    
    def send_html(self, subject, message, recipient_list, access_code, username, email_from=None, html_content=None):
        '''
            send emails with django.core.mail.EmailMultiAlternatives
        '''
        try:
            with get_connection(  
                host=settings.EMAIL_HOST, 
                port=settings.EMAIL_PORT,  
                username=settings.EMAIL_HOST_USER, 
                password=settings.EMAIL_HOST_PASSWORD, 
                use_tls=settings.EMAIL_USE_TLS  
            ) as connection:  
                subject = self.set_subject(subject).get_subject()
                email_from = self.set_from(email_from).get_from() if email_from is not None else settings.EMAIL_HOST_USER
                recipient_list = self.set_to(recipient_list).get_to()
                message = self.set_body(message).get_body()
                html_content = f"<p> \
                                    Welcome to Django Project <i><b>{username}</b></i>!.<br> \
                                    For the complete the registiration you have to submit code <br> \
                                    Your Code: <b>{self.set_access_code(access_code).get_access_code()}</b> \
                                </p>" if html_content is None else html_content
                msg = EmailMultiAlternatives(subject, message, email_from, recipient_list, connection=connection)
                msg.attach_alternative(html_content, "text/html")
                if self.get_attachment() is not None:
                    msg.attach_file(self.get_attachment())
                msg.send()
                return True
        except Exception as e:
            return False

        