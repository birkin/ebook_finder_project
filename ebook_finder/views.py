# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

log = logging.getLogger(__name__)


def api_v1( request ):
    """ Shows params. """
    callnumber = request.GET.get( 'callnumber', '' )
    title = request.GET.get( 'title', '' )
    author = request.GET.get( 'author', '' )
    jdct = {
        'callnumber': callnumber,
        'author': author,
        'title': title }
    ouput = json.dumps( jdct, sort_keys=True, indent=2 )
    return HttpResponse( ouput, content_type=u'application/javascript; charset=utf-8' )


def hi( request ):
    """ Returns simplest response. """
    now = datetime.datetime.now()
    return HttpResponse( '<p>hi</p> <p>( %s )</p>' % now )
