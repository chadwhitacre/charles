from django.conf.urls.defaults import *
from django.http import HttpResponse


def view(request, *args, **kwargs):
    return HttpResponse('Greetings, program!')

urlpatterns = patterns('', (r'^.*$', view))
