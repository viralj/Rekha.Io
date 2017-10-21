from django.core.management import BaseCommand

from plugins.jsx_compiler import RIJSXCompiler


class Command(BaseCommand):
    help = 'Command to compile all jsx files.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        j = RIJSXCompiler()
