from django.core.management import BaseCommand

from orders.tests.utils import load_fixture


class Command(BaseCommand):
    help = 'Creates dummy api data'

    def handle(self, *args, **options):
        load_fixture()
        self.stdout.write(self.style.SUCCESS('Fixture loaded successfully'))
