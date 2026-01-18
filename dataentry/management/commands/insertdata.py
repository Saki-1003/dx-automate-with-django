# adding some data to database using the custom command

from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
  help = "It will insert data to the database"

  def handle(self, *args, **kwargs):
    dataset = [
      {"roll_no": 1002, "name": "Rachel", "age": 22},
      {"roll_no": 1006, "name": "Mike", "age": 20},
      {"roll_no": 1004, "name": "Toby", "age": 21},
      {"roll_no": 1005, "name": "Ana", "age": 23},
    ]

    for data in dataset:
      roll_no = data["roll_no"]
      exisiting_record = Student.objects.filter(roll_no=roll_no).exists()
      if not exisiting_record:
        Student.objects.create(roll_no=data["roll_no"], name=data["name"], age=data["age"])
      else:
        self.stdout.write(self.style.WARNING(f"Stuendt with roll_no {roll_no} already exists!"))
    
    self.stdout.write(self.style.SUCCESS("Data inserted successfully!"))
  