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

    def check_title( self ):
        """ Makes solr title query. """
        title = urlquote( 'Zen-brain horizons : toward a living zen' )
        params = {
            'spellcheck': 'false',
            'facet': 'true',
            'sort': 'score desc, pub_date_sort desc, title_sort asc',
            'indent':'true',
            'stats':'true',
            'f.language_facet.facet.limit':'21',
            'f.topic_facet.facet.limit':'21',
            'wt':'json',
            'defType':'lucene',
            'rows':'10',
            'stats.field':'pub_date',
            # 'q':'_query_:'{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}Zen-brain horizons : toward a living zen'',
            # 'q':'_query_:"%s"' % title,
            'q':'_query_:"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}Zen-brain horizons : toward a living zen"',
            'f.author_facet.facet.limit':'21',
            'f.region_facet.facet.limit':'21',
            # 'facet.field':['access_facet',
            #   'format',
            #   'author_facet',
            #   'pub_date',
            #   'topic_facet',
            #   'region_facet',
            #   'language_facet',
            #   'building_facet'],
            # 'fq':['{!raw f=format}Book', 'access_facet:(\'Online\')'],
            'fq': ['{!raw f=format}Book', 'access_facet:("Online")'],
            'f.format.facet.limit':'11'
            }
        r = requests.get( self.SOLR_URL, params=params )
        utf8_content = r.content
        print utf8_content
        content = utf8_content.decode( 'utf-8' )
        return content

      # "spellcheck":"false",
      # "facet":"true",
      # "sort":"score desc, pub_date_sort desc, title_sort asc",
      # "indent":"true",
      # "stats":"true",
      # "f.language_facet.facet.limit":"21",
      # "f.topic_facet.facet.limit":"21",
      # "wt":["json",
      #   "ruby"],
      # "defType":"lucene",
      # "rows":"10",
      # "stats.field":"pub_date",
      # "q":"_query_:\"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}Zen-brain horizons : toward a living zen\"",
      # "f.author_facet.facet.limit":"21",
      # "f.region_facet.facet.limit":"21",
      # "facet.field":["access_facet",
      #   "format",
      #   "author_facet",
      #   "pub_date",
      #   "topic_facet",
      #   "region_facet",
      #   "language_facet",
      #   "building_facet"],
      # "fq":["{!raw f=format}Book",
      #   "access_facet:(\"Online\")"],
      # "f.format.facet.limit":"11"}},
