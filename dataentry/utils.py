from django.apps import apps
from django.core.management.base import CommandError
import csv
import hashlib
import time
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os
from emails.models import Email, Sent, EmailTracking, Subscriber
from bs4 import BeautifulSoup


def get_all_custom_models():
    default_models = ['ContentType', 'Session', 'LogEntry', 'Group', 'Permission', 'User', 'Upload']
    # get all apps
    custom_models = []
    for model in apps.get_models():
      if model.__name__ not in default_models:
        custom_models.append(model.__name__)
    return custom_models


def check_csv_errors(file_path, model_name):
    # Search for the model class accross all installed apps
    model = None
    for app_config in apps.get_app_configs():
      try:
        model = apps.get_model(app_config.label, model_name)
        break
      except LookupError:
        continue # Try next app   
    if not model:
      raise CommandError(f'Model "{model_name}" not found in any app!')

    # get all field names of the model except id
    model_fields = [field.name for field in model._meta.fields if field.name != "id"]
      
    try: 
      with open(file_path, "r") as file:
        reader = csv.DictReader(file) # DictReader takes the first row as header
        csv_header = reader.fieldnames
        # compare scv header with mode field names
        if csv_header != model_fields:
          raise DataError(f"CSV header does not match the {model_name} table fields.")
    except Exception as e:
        raise e
    
    return model


def send_email_notification(mail_subject, message, to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        # to_email をリストに変換（文字列の場合）
        if isinstance(to_email, str):
            to_email = [to_email]

        for recipient_email in to_email:
          # Create EmailTracking record for each recipient
          new_message = message

          if email_id:
            email = Email.objects.get(pk=email_id)
            subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)
            # Logic to create a unique _id
            timestamp = str(time.time())
            data_to_hash = f"{recipient_email}{timestamp}"
            unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
            email_tracking = EmailTracking.objects.create(
               email=email, 
               subscriber=subscriber, 
               unique_id=unique_id
            )

            # Generate the tracking pixel/ url
            click_tracking_url = f"{settings.BASE_URL}/emails/track/click/{unique_id}"
            # open_tracking_url = f"{settings.BASE_URL}/emails/track/open/{unique_id}"
          

            # Search for the links in the email body (email body is in HTML format since we set the content type to HTML in the send_emails view) 
            # so to scrape information from html we can use BeautifulSoup library
            soup = BeautifulSoup(message, 'html.parser')

            # Find all the anchor tags('a') with href 
            # this will give us a list of all the urls(eg. https://google.com) in the email body  
            urls = [link['href'] for link in soup.find_all('a', href=True)] 

            # If there are links or urls in the email body, inject our click tracking url to the links
            if urls:  
              for url in urls:
                  # Injecting the click tracking url to the original url. 
                  tracking_url =f"{click_tracking_url}?url={url}"
                  new_message = new_message.replace(f"{url}", f"{tracking_url}")

            else:
              print("No links found in the email body.")

            # Create an emai content with tracking url/pixel image
            # open_tracking_img = f"<img src='{open_tracking_url}' width='1 height='1' />" 
            # new_message += open_tracking_img

          # When the recipient clicks the link, it will first hit our click tracking url, 
          # then we can store the click info in the database and finally redirect to the original url.
          mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email])
          if attachment is not None:
            mail.attach_file(attachment)

          mail.content_subtype = "html" # Set the email content type to HTML
          mail.send()

        # Store the total sent emails inside the Sent model
        if email:
          email = Email.objects.get(pk=email_id)
          sent = Sent()
          sent.email = email
          sent.total_sent = email.email_list.count_emails()
          sent.save()

    except Exception as e:
       raise e
    

def generate_csv_file(model_name):
    # generate timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # define the csv file name
    export_dir = 'exported_data' # directory name to store the exported data
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    print('file_path:', file_path)
    return file_path