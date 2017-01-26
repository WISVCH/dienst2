from django_seed import Seed
from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(selfself, *args, **options):
        seeder = Seed.seeder()

        import ldb.models as model

        seeder.add_entity(model.Entity, 100)

        seeder.add_entity(model.Organization, 10)

        seeder.add_entity(model.Person, 10, {
            'living_with': lambda x: None
        })

        # seeder.add_entity(model.Member, 10)
        # seeder.add_entity(model.Student, 10)
        # seeder.add_entity(model.Alumnus, 10)
        # seeder.add_entity(model.Employee, 10)


        # seeder.add_entity(model.Modification, 10)
        # seeder.add_entity(model.Committee, 10)
        # seeder.add_entity(model.CommitteeMembership, 10)


        inserted_pks = seeder.execute()
