import atexit
import logging
import os
import socket
import sys
import traceback

import charles
import django
from charles import __version__, restarter
from charles import settings as charles_settings
from charles.wsgiserver import CherryPyWSGIServer as BaseServer
from django.conf import settings as django_settings
from django.core.handlers.wsgi import WSGIHandler


log = logging.getLogger('charles.server')


class Server(BaseServer):

    def __init__(self):
        """Extend to take a Django settings object.
        """

        django_version = "Django/%s" % django.get_version()
        charles_version = "Charles/%s" % __version__
        self.version = ', '.join(( django_version
                                 , charles_version
                                 , self.version
                                  ))

        # super() vs. BaseClass.__init__():
        # http://mail.python.org/pipermail/python-list/2006-February/367002.html
        BaseServer.__init__( self
                           , charles_settings.ADDRESS
                           , WSGIHandler()
                           , charles_settings.THREADS
                            )
    
        atexit.register(self.stop)
   

    def start(self):
        """Extend to support filesystem monitoring.
        """
        log.warn("starting on %s" % str(charles_settings.ADDRESS))
   
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
        if not charles.WINDOWS: 
            if charles_settings.SOCKFAM == socket.AF_UNIX: # prune socket
                try:
                    os.remove(charles_settings.ADDRESS)
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

