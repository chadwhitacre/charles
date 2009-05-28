from charles.ipc.pidfile import PIDFileMissing, State
from charles.management.commands import pidfile
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            child_pid = pidfile.getpid()
            retcode = 0
        except PIDFileMissing:
            print "daemon not running (no pidfile)"
            retcode = 0
        except State, state:
            print state
            retcode = 1
        else:
            print "daemon running with pid %d" % child_pid
        raise SystemExit(retcode)
 
