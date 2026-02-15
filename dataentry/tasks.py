from dx_automation_main.celery import app
from django.core.management import call_command # to run management commands
from .utils import send_email_notification
from django.conf import settings
from dataentry.utils import generate_csv_file 


@app.task # This decorator makes this function a Celery task
def import_data_task(file_path, model_name):
    try:
      # call the management command to import data
      call_command('importdata', file_path, model_name)
    except Exception as e:
      raise e
    
    # notify the success of the task by email
    mail_subject = 'Data Import Successful'
    message = 'Your data import has been completed successfully'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)

    return 'Data import task completed'

@app.task
def export_data_task(model_name):
    try:
      call_command('exportdata', model_name)
    except Exception as e:
      raise e
    
    file_path =generate_csv_file(model_name)

    
    # send email with the attachement of the exported data
    mail_subject = 'Export data successful'
    message = 'Your data export has been completed successfully. Please find the exported data attached.'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email, attachment=file_path)
    return 'Export data task completed successfully'
