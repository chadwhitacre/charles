"""Main loop
"""
import atexit
import logging
import os
import sys
import tempfile
import traceback


__version__ = '0.1' # our subpackages use this
WINDOWS = 'win32' in sys.platform  # this also


from charles.ipc import restarter
from charles.ipc.pidfile import PIDFile
from charles.server import Server


log = logging.getLogger('charles')


# Main
# ====

def absolutize_root(argv):
    """Absolutize any --root given in argv.

    We need to absolutize any root path, because when we daemonize we chdir in 
    the daemon/parent, so if --root is relative it will break in the child.

    We only run this when we are daemonizing. It will have been validated by 
    OptParse by then.

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


def main_loop(configuration):
    """Given a configuration object, do daemony things and go into a loop.
    """
    if restarter.PARENT:

        argv = sys.argv[:]

        if configuration.daemon is not None:
            argv = absolutize_root(argv)
            configuration.daemon.drive() # will daemonize or raise SystemExit

        restarter.loop(argv)

    else:
        assert restarter.CHILD # sanity check

        if configuration.daemon is not None:
            configuration.pidfile.write() # only in CHILD of daemon
            atexit.register(configuration.pidfile.remove)

        server = Server(configuration)
        server.start()


def main(argv=None):
    """Run the main loop safely.
    """
    try:
        main_loop()
    except SystemExit, exc:
        if exc.code == 0:
            log_func = log.debug
        if exc.code != 0:
            log_func = log.info
        
        tb = sys.exc_info()[2]
        while tb.tb_next is not None:
            tb = tb.tb_next
        frame = tb.tb_frame
        filename = os.path.basename(frame.f_code.co_filename)
        location = "%s:%s" % (filename, frame.f_lineno)
        log_func("exiting with exit code %d (from %s)" % (exc.code, location))

        raise # fyi, without this child wasn't terminating

    except KeyboardInterrupt:
        pass
    except:
        log.critical(traceback.format_exc())
        sys.exit(1)

