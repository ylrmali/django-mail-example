from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('send_email/', views.send_email, name='send_email'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('confirm/', views.confirm, name='confirm'),
]