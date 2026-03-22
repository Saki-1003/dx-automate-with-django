from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os


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


def send_email_notification(mail_subject, message, to_email, attachment=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        # to_email をリストに変換（文字列の場合）
        if isinstance(to_email, str):
            to_email = [to_email]
        mail = EmailMessage(mail_subject, message, from_email, to=to_email)
        if attachment is not None:
           mail.attach_file(attachment)
        mail.content_subtype = "html" # Set the email content type to HTML
        mail.send()
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