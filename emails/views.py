from django.shortcuts import render
from .forms import EmailForm
from django.contrib import messages
from django.shortcuts import redirect
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber
from .tasks import send_email_task

# Create your views here.
def send_emails(request): 
  if request.method == 'POST':
    email_form = EmailForm(request.POST, request.FILES)

    if email_form.is_valid():
      email_form = email_form.save()
      # Send an email here using the data from the form
      mail_subject = request.POST.get('subject') # inside the brackets, the name should be the same as the name attribute in the HTML form field
      message = request.POST.get('body')
      email_list = request.POST.get('email_list')
      
      # Access the selected email list and retrieve the email addresses
      email_list = email_form.email_list
      
      # Extract email addresses from the Subscriber model based on the selected email list
      subscribers = Subscriber.objects.filter(email_list=email_list)

      to_email = [subscriber.email_address for subscriber in subscribers]
      # for subscriber in subscribers:
      #   to_email.append(subscriber.email_address)

      if email_form.attachment:
        # Get the file path of the uploaded attachment from media folder
        attachment = email_form.attachment.path 
      else:
        attachment = None
      # Handover email sending task to Celery worker
      send_email_task.delay(mail_subject, message, to_email, attachment)

      # Display a success message
      messages.success(request, "Email sent successfully")
      return redirect('send_emails')

  else: 
    email_form = EmailForm() #forms.pyで定義したformクラスをインスタンス化
    context = {
      'email_form': email_form
    }
  return render(request, 'emails/send_emails.html', context)