from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<arg1 arg2 ...>'
    help = 'Command to do ...'

    def handle(self, *args, **options):

        self.stdout.write('Job complete')