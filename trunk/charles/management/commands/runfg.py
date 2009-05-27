from charles.server import Server


from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        import settings
        server = Server(settings)
        server.start()

