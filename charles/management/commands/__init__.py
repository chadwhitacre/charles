"""Manipulate a daemon via a pidfile, or become one ourselves.

Note that on principle we don't remove bad pidfiles, because they indicate a
bug, and are potentially useful for debugging.

If the command is 'start' or 'runserver' we proceed with the program. Stop,
restart, and status will raise SystemExit.

"""
import os

import charles
from charles.ipc.daemon import Daemon
from charles.ipc.pidfile import PIDFile


# PIDFile
# =======
# This only gets written in CHILD of a daemon.

pidpath = os.path.abspath('django.pid')
pidfile = PIDFile(pidpath)
pidfile = pidfile


# Daemon
# ======

if not charles.WINDOWS:
    root = os.getcwd()
    daemon = Daemon(pidfile, root)

