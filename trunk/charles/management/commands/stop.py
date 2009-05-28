from charles.ipc.pidfile import State
from charles.management.commands import daemon
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            retcode = daemon.stop()
        except State, state:
            print state
            retcode = 1 
        raise SystemExit(retcode)

