from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
import datetime
import csv

# command - python manage.py exportdata <model_name>
class Command(BaseCommand):
  help = "Export data from the database to a CSV file"

  def add_arguments(self, parser):
    parser.add_argument('model_name', type=str, help='Model name')

  def handle(self, *args, **kwargs):
    model_name = kwargs['model_name'].capitalize()

    # search through all the installed apps for the model
    model = None
    for app_config in apps.get_app_configs():
      try: 
        model = apps.get_model(app_config.label, model_name)
        break # model found, exit loop
      except LookupError:
        pass # try next app
    
    if not model:
      self.stderr.write(f'Model "{model_name}" not found in any app!\n')
      return

    # fetch the data from db
    data = model.objects.all()

    # generate timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # define the csv file name
    file_path = f'exported_{model_name}_data_{timestamp}.csv'

    # open the csv file and write the data
    with open(file_path, 'w', newline='') as file:
      writer = csv.writer(file)

      # write the header
      writer.writerow([field.name for field in model._meta.fields]) # _meta.fields is a django method that gives model's all fields

      # write data rows
      for dt in data:
        writer.writerow([getattr(dt, field.name)for field in model._meta.fields])

    self.stdout.write(self.style.SUCCESS(f'Data exported successfully to {file_path}'))