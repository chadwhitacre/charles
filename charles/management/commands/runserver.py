import sys

from charles.server import Server
from charles.ipc import restarter
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        if restarter.PARENT:
            argv = sys.argv[:]
            restarter.loop(argv)
        else:
            assert restarter.CHILD # sanity check
            import settings
            server = Server(settings)
            server.start()

