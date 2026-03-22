from django.urls import path
from . import views

urlpatterns = [
  path('send_emails/', views.send_emails, name='send_emails')
]