# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint, itertools
import requests
# from django.conf import settings as project_settings
# from django.core.urlresolvers import reverse
# from django.db import models
# from django.http import HttpResponseRedirect
# from django.utils.encoding import smart_unicode
# from django.utils.http import urlquote
# from django.utils.text import slugify

log = logging.getLogger(__name__)


class Processor( object ):
    """ Manages processing. """

    def determine_handler( self, callnumber, title, author ):
        """ Determines which kind of query to run.
            Called by views.api_v1() """
        if callnumber is not '':
            handler = { 'callnumber': callnumber }
        elif title is not '' and author is '':
            handler = { 'title': title }
        elif title is not '' and author is not '':
            handler = { 'title_and_author': {'title': title, 'author': author} }
        else:
            raise Exception( 'params problem' )
        return handler

    def process_request( self, handler ):
        """ Manages processing flow.
            Called by views.api_v1() """
        slr = SolrAccessor()
        params = self.build_params( handler )
        raw_data_dct = json.loads( slr.run_query(params) )
        log.debug( 'raw_data_dct, ```%s```' % pprint.pformat(raw_data_dct) )
        massaged_data_dct = self.massage_data( raw_data_dct )
        return massaged_data_dct

    def build_params( self, handler ):
        """ Manages params building.
            Called by process_request() """
        slr = SolrAccessor()
        if handler.keys()[0] == 'title':
            params = slr.build_title_params( handler['title'] )
        elif handler.keys()[0] == 'title_and_author':
            params = slr.build_title_and_author_params( handler['title_and_author'] )
        return params

    def massage_data( self, raw_data_dct ):
        """ Extracts required data from solr response.
            Called by process_request() """
        items = []
        for raw_item in raw_data_dct['response']['docs']:
            item = {}
            item['title'] = raw_item['title_display']
            item['url'] = raw_item['url_fulltext_display'][0]
            item['author'] = raw_item.get( 'author_display', 'no_author_listed' )
            items.append( item )
        return items

    # end class Processor


class SolrAccessor( object ):
    """ Handles solr queries. """

    def __init__( self ):
        self.SOLR_URL = os.environ['EBK_FNDR__SOLR_URL']
        self.standard_params = {
            'sort': 'score desc, pub_date_sort desc, title_sort asc',
            'indent':'true',
            'wt':'json',
            'defType':'lucene',
            'rows':'10',
            'q':'',
            'f.author_facet.facet.limit':'21',
            'fq': ['{!raw f=format}Book', 'access_facet:("Online")'],
            }

    def build_title_params( self, title ):
        """ Makes title query params.
            Called by Processor.process_request() """
        params = self.standard_params.copy()
        params['q'] = '_query_:"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}%s"' % title
        # params['q'] = requests.utils.quote( '_query_:"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}%s"' % title, safe='_:"' )
        return params

    def build_title_and_author_params( self, title_author_dct ):
        """ Makes title query params.
            Called by Processor.process_request() """
        title = title_author_dct['title']
        author = title_author_dct['author']
        params = self.standard_params.copy()
        params['q'] = '_query_:"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}%s" AND _query_:"{!dismax spellcheck.dictionary=author qf=$author_qf pf=$author_pf}%s"' % ( title, author )
        return params

    def run_query( self, params ):
        """ Runs solr query & returns json.
            Called by Processor.process_request() """
        r = requests.get( self.SOLR_URL, params=params )
        log.debug( 'solr_url, `%s`' % r.url )
        utf8_content = r.content
        print utf8_content
        return utf8_content

    # end class SolrAccessor
