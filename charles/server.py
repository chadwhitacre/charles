import atexit
import logging
import os
import socket
import sys
import traceback

import django
from charles import __version__, restarter, settings
from charles.wsgiserver import CherryPyWSGIServer as BaseServer
from django.conf import settings as django_settings
from django.core.handlers.wsgi import WSGIHandler


log = logging.getLogger('charles.server')


class Server(BaseServer):

    def __init__(self):
        """Extend to take a Django settings object.
        """

        self.version = "Django-%s/Charles-%s" % ( django.get_version()
                                                , __version__
                                                 )

        # super() vs. BaseClass.__init__():
        # http://mail.python.org/pipermail/python-list/2006-February/367002.html
        BaseServer.__init__( self
                           , settings.ADDRESS
                           , WSGIHandler()
                           , settings.THREADS
                            )
    
        atexit.register(self.stop)
   

    def start(self):
        """Extend to support filesystem monitoring.
        """
        log.warn("starting on %s" % str(settings.ADDRESS))
   
        if django_settings.DEBUG:
            log.info("configuring filesystem monitor")
            paths = []
            for path in paths:
                if os.path.isfile(path):
                    restarter.monitor(path)
            restarter.start_monitoring()
        
        BaseServer.start(self)


    def stop(self):
        """Extend for additional cleanup.
        """
        log.debug("cleaning up server")
        sys.stdout.flush()
        BaseServer.stop(self)
        if 'win' not in sys.platform: 
            if settings.SOCKFAM == socket.AF_UNIX: # prune socket
                try:
                    os.remove(settings.ADDRESS)
                except EnvironmentError, exc:
                    log.error("error removing socket:", exc.strerror)
        # pidfile removed in __init__.py:main_loop
        # restarter stopped in restarter.py:_atexit


    if restarter.CHILD:
        def tick(self):
            """Extend to support restarting when we are restarter.CHILD.

            Note that when using aspen.main_loop, Server is only ever
            instantiated within restarter.CHILD.

            """
            BaseServer.tick(self)
            if restarter.should_restart():
                log.info("restarting")
                raise SystemExit(75) # will trigger self.stop via atexit

