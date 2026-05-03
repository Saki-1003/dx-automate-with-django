from django.core.management.base import BaseCommand
from django.apps import apps
from dataentry.utils import check_csv_errors
import csv
import chardet


# command - python manage.py importdata <file_path> <model_name>
class Command(BaseCommand):
  help = "Import data from CSV file"

  def add_arguments(self, parser):
    parser.add_argument("file_path", type=str, help="Path to the CSV file")
    parser.add_argument("model_name", type=str, help="Name of the model")

  def handle(self, *args, **kwargs):
    file_path = kwargs["file_path"]
    model_name = kwargs["model_name"].capitalize()
    
    model = check_csv_errors(file_path, model_name)
   
    # Detect file encoding
    with open(file_path, "rb") as f:
      raw_data = f.read()
      result = chardet.detect(raw_data)
      encoding = result.get('encoding', 'utf-8')
    
    with open(file_path, "r", encoding=encoding) as file:
      reader = csv.DictReader(file)
      for row in reader:
        model.objects.create(**row)

    self.stdout.write(self.style.SUCCESS("Data imported from CSV successfully!"))
