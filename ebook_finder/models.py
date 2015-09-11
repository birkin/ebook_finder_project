# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint, itertools
import requests
from django.conf import settings as project_settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_unicode
from django.utils.http import urlquote
from django.utils.text import slugify

log = logging.getLogger(__name__)


class SolrAccessor( object ):
    """ Handles solr queries. """

    def __init__( self ):
        self.SOLR_URL = os.environ['EBK_FNDR__SOLR_URL']

    def check_title( self, title ):
        """ Makes solr title query. """
        params = {
            'sort': 'score desc, pub_date_sort desc, title_sort asc',
            'indent':'true',
            'wt':'json',
            'defType':'lucene',
            'rows':'10',
            'q':'_query_:"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}%s"' % title,
            'f.author_facet.facet.limit':'21',
            'fq': ['{!raw f=format}Book', 'access_facet:("Online")'],
            }
        r = requests.get( self.SOLR_URL, params=params )
        utf8_content = r.content
        print utf8_content
        content = utf8_content.decode( 'utf-8' )
        return content

    # def check_title( self ):
    #     """ Makes solr title query. """
    #     params = {
    #         'sort': 'score desc, pub_date_sort desc, title_sort asc',
    #         'indent':'true',
    #         'wt':'json',
    #         'defType':'lucene',
    #         'rows':'10',
    #         'q':'_query_:"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}Zen-brain horizons : toward a living zen"',
    #         'f.author_facet.facet.limit':'21',
    #         'fq': ['{!raw f=format}Book', 'access_facet:("Online")'],
    #         }
    #     r = requests.get( self.SOLR_URL, params=params )
    #     utf8_content = r.content
    #     print utf8_content
    #     content = utf8_content.decode( 'utf-8' )
    #     return content

    # end class SolrAccessor
