from django.core.management.base import BaseCommand

class Command(BaseCommand):
  help = "Prints hellow World"

  def handle(self, *args, **kwargs):
    self.stdout.write("Hello World!")