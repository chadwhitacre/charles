import atexit
import sys

from charles.ipc import restarter
from charles.ipc.pidfile import PIDFileMissing, State
from charles.management.commands import daemon, pidfile
from charles.server import Server
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        if restarter.PARENT:
    
            argv = sys.argv[:]
            argv = self.absolutize_root(argv) #@: no-op for now

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
            restarter.loop(argv)
    
        else:
            assert restarter.CHILD # sanity check
    
            pidfile.write() # only in CHILD of daemon
            atexit.register(pidfile.remove)
    
            import settings
            server = Server(settings)
            server.start()


    def absolutize_root(self, argv):
        """Absolutize any --root given in argv.
    
        We need to absolutize any root path, because when we daemonize we chdir
        in the daemon/parent, so if --root is relative it will break in the
        child.
    
        We only run this when we are daemonizing. It will have been validated
        by OptParse by then.
    
        """
        for i in range(len(argv)):
            val = argv[i]
            if val in ('-r', '--root'):
                root = argv[i+1]
                argv[i+1] = os.path.realpath(root)
                break
            elif val.startswith('-r'):
                root = val[len('-r'):]
                argv[i] = '-r%s' % os.path.realpath(root)
                break
            elif val.startswith('--root='):
                root = val[len('--root='):]
                argv[i] = '--root=%s' % os.path.realpath(root)
                break
        return argv
    
