"""Wrapper for using the django settings.py module in charles.

Ref:

    http://docs.djangoproject.com/en/1.0/topics/settings/

"""
import os
import socket

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured


# Validation routines
# ===================

def validate_address(address):
    """Given a tuple or string, raise ImproperlyConfigured or return a tuple.

    The returned tuple is (address, sockfam).

    """

    if isinstance(address, basestring):                         
        
        # AF_UNIX
        # =======
        # We could test to see if the path exists or is creatable, etc.

        if address[0] in ('/','.'):
            if WINDOWS:
                msg = "You can't use an AF_UNIX socket on Windows."
                raise ImproperlyConfigured(msg)
                #@: But what about named pipes?
        sockfam = socket.AF_UNIX
        address = os.path.realpath(address)


    elif (len(address) > 2) or (address[0].count(':') > 1):     
        
        # AF_INET6
        # ========

        sockfam = socket.AF_INET6
        # @@: validate this, eh?


    else:                                                       
        
        # AF_INET
        # =======
        # Here we need a tuple: (str, int). The string must be a valid IPv4 
        # address or the empty string, and the int (the port) must be between 0 
        # and 65535, inclusive.

        msg = "SERVER_ADDRESS is not valid: %s" % (address,)
        exc = ImproperlyConfigured(msg)

        if len(address) not in (1, 2):
            raise exc
        if not isinstance(address, (tuple, list)):
            raise exc

        if len(address) == 1:
            address += (8000,) # default port

        ip, port = address # split for validation


        # IP
        # ==

        if not isinstance(ip, basestring):
            raise exc 
        elif ip == '':
            ip = '0.0.0.0' # IP defaults to INADDR_ANY for AF_INET; specified
                           # explicitly to avoid accidentally binding to
                           # INADDR_ANY for AF_INET6.
                           #
                           # 2009-05-28: not exactly sure what this means 
                           # anymore, but leaving it in anyway. :) (I have a 
                           # vague recollection that it has to do with 
                           # triggering behavior in wsgiserver.py?) [cwlw]
        else:
            try:
                socket.inet_aton(ip)
            except socket.error:
                raise exc 


        # port
        # ====
        # Coerce to int. Must be between 0 and 65535, inclusive. 
        
        try:
            port = int(port)
        except (TypeError, ValueError):
            raise exc
        
        if not(0 <= port <= 65535):
            raise exc


        # Success!
        # ========

        address = (ip, port)
        sockfam = socket.AF_INET


    return (address, sockfam)


def validate_threads(threads):
    """Given an object, raise ImproperlyConfigured or return an int.
    """
    msg = "SERVER_THREADS is not an int greater than one: %s" % threads
    exc = ImproperlyConfigured(msg)
    if not isinstance(threads, (int, long)):
        raise exc
    if not threads >= 1:
        raise exc
    return threads


# Access with defaults
# ====================

defaults = dict()
defaults['SERVER_ADDRESS'] = ('', 8000)
defaults['SERVER_THREADS'] = 10
defaults['SERVER_USER'] = ''
defaults['SERVER_GROUP'] = ''
defaults['SERVER_SSL_CERTIFICATE'] = ''
defaults['SERVER_SSL_PRIVATE_KEY'] = ''
defaults['SERVER_DAEMON_DIRECTORY'] = '.'
defaults['SERVER_DAEMON_STDOUT'] = '/dev/null'
defaults['SERVER_DAEMON_STDERR'] = None # None means 'same as stdout'


def get(name):
    """Given a string, return a Django setting or a default.
    """
    try:
        out = getattr(django_settings, name)
    except AttributeError:
        out = defaults[name]
    return out


ADDRESS, SOCKFAM = validate_address(get('SERVER_ADDRESS'))
THREADS = validate_threads(get('SERVER_THREADS'))

