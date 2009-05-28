from django.conf.urls.defaults import *
from django.http import HttpResponse


def view(request, *args, **kwargs):
    return HttpResponse('<p>Greetings, program!</p>')

urlpatterns = patterns('', (r'^.*$', view))
