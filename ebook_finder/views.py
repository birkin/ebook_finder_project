# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint
import requests
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from ebook_finder.models import Processor


log = logging.getLogger(__name__)

processor = Processor()


def api_v1( request, verbosity ):
    """ Returns ebook info for given params. """
    log.debug( 'starting' )
    handler = processor.determine_handler(
        callnumber=request.GET.get( 'callnumber', '' ),
        title=request.GET.get( 'title', '' ),
        author=request.GET.get( 'author', '' ) )
    data_dct = processor.process_request( verbosity, handler )
    output = processor.build_response( request, handler, data_dct )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def api_v2( request, verbosity ):
    """ Returns ebook info for given params -- using `.json` of josiah-blacklight. """
    log.debug( 'starting' )
    handler = processor.determine_handler(
        callnumber=request.GET.get( 'callnumber', '' ),
        title=request.GET.get( 'title', '' ),
        author=request.GET.get( 'author', '' ) )
    # data_dct = processor.process_request_v2( verbosity, handler )
    # output = processor.build_response( request, handler, data_dct )
    output = json.dumps( {'response': 'coming'} )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def hi( request ):
    """ Returns simplest response. """
    now = datetime.datetime.now()
    return HttpResponse( '<p>hi</p> <p>( %s )</p>' % now )
