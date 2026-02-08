from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
import csv
from django.db import DataError

# command - python manage.py importdata <file_path> <model_name>
class Command(BaseCommand):
  help = "Import data from CSV file"

  def add_arguments(self, parser):
    parser.add_argument("file_path", type=str, help="Path to the CSV file")
    parser.add_argument("model_name", type=str, help="Name of the model")

  def handle(self, *args, **kwargs):
    file_path = kwargs["file_path"]
    model_name = kwargs["model_name"].capitalize()

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
    
    # compare scv header with mode field names
    model_fields = [field.name for field in model._meta.fields if field.name != "id"]
    print(model_fields)
      
    with open(file_path, "r") as file:
      reader = csv.DictReader(file) # DictReader takes the first row as header
      csv_header = reader.fieldnames

      # compare csv heade with model's field names
      if csv_header != model_fields:
        raise DataError(f"CSV header does not match the {model_name} table fields.")




      for row in reader:
        model.objects.create(**row)
    self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully!"))
