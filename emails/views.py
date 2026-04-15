from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmailForm
from django.contrib import messages
from django.shortcuts import redirect
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber, Email, Sent, EmailTracking
from .tasks import send_email_task
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def send_emails(request): 
  if request.method == 'POST':
    email_form = EmailForm(request.POST, request.FILES)

    if email_form.is_valid():
      email = email_form.save()
      # Send an email here using the data from the form
      mail_subject = request.POST.get('subject') # inside the brackets, the name should be the same as the name attribute in the HTML form field
      message = request.POST.get('body')
      email_list = request.POST.get('email_list')
      
      # Access the selected email list and retrieve the email addresses
      email_list = email.email_list
      
      # Extract email addresses from the Subscriber model based on the selected email list
      subscribers = Subscriber.objects.filter(email_list=email_list)

      to_email = [subscriber.email_address for subscriber in subscribers]
      # for subscriber in subscribers:
      #   to_email.append(subscriber.email_address)

      if email.attachment:
        # Get the file path of the uploaded attachment from media folder
        attachment = email.attachment.path 
      else:
        attachment = None

      email_id = email.id

      # Handover email sending task to Celery worker
      send_email_task.delay(mail_subject, message, to_email, attachment, email_id)

      # Display a success message
      messages.success(request, "Email sent successfully")
      return redirect('send_emails')

  else: 
    email = EmailForm() #forms.pyで定義したformクラスをインスタンス化
    context = {
      'email_form': email,
    }
  return render(request, 'emails/send_emails.html', context)


def track_click(request, unique_id):
  # logic to store the tracking info
  try:
    email_tracking = EmailTracking.objects.get(unique_id=unique_id)
    # クエリパラメータから元のURLを取得
    url = request.GET.get('url')
    # Check whether the clicke_at is alrady set
    if not email_tracking.clicked_at:
      email_tracking.clicked_at = timezone.now()
      email_tracking.save()
      # Redirect to the original url after storing the click info in the database
      return HttpResponseRedirect(url) 
    else: 
      # If clicked_at is already set, redirect to the original url withiout saving anything.
      return HttpResponseRedirect(url)
  except:
    pass
  


# def track_open(request, unique_id):
#   try:
#     email_tracking = EmailTracking.objects.get(unique_id=unique_id)
#     # Check whether the opned_at field is alredy set
#     if not email_tracking.opend_at:
#       email_tracking.opend_at = timezone.now()
#       email_tracking.save()
#       return HttpResponse("Email open tracked successfully.")
#     else:
#       print("Email already opned")
#       return HttpResponse("Email already opned.")

#   except EmailTracking.DoesNotExist:
#     return HttpResponse("Email tracking record not found!")


def track_dashboard(request):
  # Reverse lookup (from child to parent)
  emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent')) # This will assign the total_sent field to each email object
  context = {
    'emails': emails,
  }
  return render(request, 'emails/track_dashboard.html', context)


def track_stats(request, pk):
  email = get_object_or_404(Email, pk=pk)
  sent = Sent.objects.get(email=email)
  context = {
    'email': email,
    'total_sent': sent.total_sent,
  }
  return render(request, 'emails/track_stats.html', context)