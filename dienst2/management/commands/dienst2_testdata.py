from django.core.management import BaseCommand
from django_seed import Seed

from post.models import Item, Contact, Category

try:
    # import django settings
    from django.conf import settings
    # check if timezone is active
    if getattr(settings, 'USE_TZ', False):
        # make datetime timezone aware
        from django.utils import timezone
        _timezone_format = lambda value: timezone.make_aware(
            value, timezone.get_current_timezone()
        )
    else:
        # keep value as is
        _timezone_format = lambda x: x
except ImportError:
    # django not available, keep value as is
    _timezone_format = lambda x: x

class Command(BaseCommand):
    def handle(self, *args, **options):
        seeder = Seed.seeder()

        seeder.add_entity(Contact, 40, {
            'name': lambda x: seeder.faker.company()
        })
        seeder.add_entity(Category, 15, {
            'name': lambda x: seeder.faker.job()
        })
        seeder.add_entity(Item, 300, {
            'date': lambda x: _timezone_format(seeder.faker.date_time_between(start_date='-1y')),
            'description': lambda x: seeder.faker.sentence(nb_words=3)
        })

        seeder.execute()
