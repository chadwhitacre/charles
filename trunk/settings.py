import logging


# Minimal Settings
# ================
# This is the minimum needed for the charles distribution itself to run as a
# Django project.

logging.basicConfig(level=0)

DEBUG = True
INSTALLED_APPS = ['charles']
ROOT_URLCONF = 'urls'


# Address
# =======
# This can be any type of address that Python supports. The format varies based
# on the socket family, and the socket family is inferred from the format of
# the setting:
#
#   AF_INET     ('127.0.0.1', 8080)
#   AF_INET6    ('::1', 8080)
#   AF_UNIX     /path/to/socket
#
# The address will be interpreted as AF_INET6 if it has more than 2 elements, 
# or if there is a colon in the first element (the host). See also paragraph
# four and following of:
#
#   http://docs.python.org/library/socket.html

SERVER_ADDRESS = ('', 8000)


# Threads
# =======
# Charles uses a thread pool to serve requests. This settings indicates the
# size of the thread pool.

SERVER_THREADS = 10


# User and Group
# ==============
# If you start django/charles as root, then it will drop privileges using these 
# settings if provided. This happens after it binds to its port.

SERVER_USER = ''
SERVER_GROUP = ''


# SSL
# ===
# These are paths to your certificate and private key files. If provided then
# django/charles will use SSL. They must both be provided.

SERVER_SSL_CERTIFICATE = ''
SERVER_SSL_PRIVATE_KEY = ''


# Daemon
# ======
# If you start django/charles as a daemon, it will switch to the directory 
# given here, and redirect stdout/stderr to the files named. Stderr is sent to
# the same place as stdout unless set otherwise here.

SERVER_DAEMON_DIRECTORY = '.'
SERVER_DAEMON_STDOUT = '/dev/null'
SERVER_DAEMON_STDERR = None # None means 'same as stdout'

