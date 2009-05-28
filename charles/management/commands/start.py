from charles.ipc.pidfile import PIDFileMissing, State
from charles.management.commands import daemon, pidfile
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            child_pid = pidfile.getpid()
        except PIDFileMissing:
            pass # best case
        except State, state:
            print "bad pidfile: %s" % state
            raise SystemExit(1)
        else:
            print "daemon already running with pid %d" % child_pid
            raise SystemExit(1)
        daemon.start()

