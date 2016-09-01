# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint, itertools
import requests

log = logging.getLogger(__name__)


class Processor( object ):
    """ Manages processing. """

    def __init__( self ):
        self.slr = SolrAccessor()

    def determine_handler( self, callnumber, title, author ):
        """ Determines which kind of query to run, and populates dct.
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

    def process_request( self, verbosity, handler ):
        """ Manages processing flow.
            Called by views.api_v1() """
        params = self.build_params( handler )
        if params is None:
            return []
        raw_data_dct = json.loads( self.slr.run_query(params) )
        log.debug( 'raw_data_dct, ```%s```' % pprint.pformat(raw_data_dct) )
        massaged_data = self.massage_data( verbosity, raw_data_dct )
        log.debug( 'massaged_data, ```%s```' % pprint.pformat(massaged_data) )
        return massaged_data

    def build_params( self, handler ):
        """ Manages params building.
            Called by process_request() """
        handler_key = handler.keys()[0]
        if handler_key == 'title':
            params = self.slr.build_title_params( handler['title'] )
        elif handler_key == 'title_and_author':
            params = self.slr.build_title_and_author_params( handler['title_and_author'] )
        else:
            callnumber_title_author_dct = self.slr.query_callnumber( handler['callnumber'] )
            params = self.slr.build_title_and_author_params( callnumber_title_author_dct )
        return params

    def massage_data( self, verbosity, raw_data_dct ):
        """ Extracts required data from solr response.
            Called by process_request() """
        items = []
        for raw_item in raw_data_dct['response']['docs']:
            if not 'url_fulltext_display' in raw_item.keys():
                log.debug( 'no `url_fulltext_display` key found; skipping entry' )
                continue
            item = self.make_basic_item( raw_item )
            if verbosity == 'full' or verbosity == 'full/':
                item['pub_date'] = raw_item.get( 'pub_date', '' )
                item['language'] = raw_item.get( 'language_facet', '' )
            items.append( item )
        return items

    def make_basic_item( self, raw_item ):
        """ Initializes basic item-dict.
            Called by massage_data() """
        item = {}
        item['title'] = raw_item['title_display']
        item['url'] = raw_item['url_fulltext_display'][0]
        item['author'] = raw_item.get( 'author_display', 'no_author_listed' )
        item['bib'] = raw_item['id']
        return item

    # def massage_data( self, verbosity, raw_data_dct ):
    #     """ Extracts required data from solr response.
    #         Called by process_request() """
    #     items = []
    #     for raw_item in raw_data_dct['response']['docs']:
    #         item = self.make_basic_item( raw_item )
    #         if verbosity == 'full' or verbosity == 'full/':
    #             item['pub_date'] = raw_item.get( 'pub_date', '' )
    #             item['language'] = raw_item.get( 'language_facet', '' )
    #         items.append( item )
    #     return items

    # def make_basic_item( self, raw_item ):
    #     """ Initializes basic item-dict.
    #         Called by massage_data() """
    #     item = {}
    #     item['title'] = raw_item['title_display']
    #     item['url'] = raw_item['url_fulltext_display'][0]
    #     item['author'] = raw_item.get( 'author_display', 'no_author_listed' )
    #     item['bib'] = raw_item['id']
    #     return item

    def build_response( self, request, handler_dct, data_dct ):
        """ Builds response json.
            Called by views.api_v1() """
        DOCS_URL = os.environ['EBK_FNDR__DOCS']
        url = '%s://%s%s' % ( request.scheme, request.META['SERVER_NAME'], request.path )
        query_string = request.META['QUERY_STRING']
        if query_string is not None:
            url = '%s?%s' % ( url, query_string )
        request_dct = { 'url': url, 'params_used': handler_dct, 'datetime': unicode( datetime.datetime.now() ) }
        response_dct = { 'data': data_dct, 'info': DOCS_URL }
        return_dct = { 'request': request_dct, 'response': response_dct }
        output = json.dumps( return_dct, sort_keys=True, indent=2 )
        return output

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
        return params

    def build_title_and_author_params( self, title_author_dct ):
        """ Makes title/author query params.
            Called by Processor.process_request() """
        if title_author_dct is None:  # callnumber lookup returned nothing
            log.debug( 'returning None' )
            return None
        title = title_author_dct['title']
        author = title_author_dct['author']
        params = self.standard_params.copy()
        params['q'] = '_query_:"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}%s" AND _query_:"{!dismax spellcheck.dictionary=author qf=$author_qf pf=$author_pf}%s"' % ( title, author )
        return params

    def query_callnumber( self, callnumber ):
        """ Tries to get title and author from callnumber; returns title/author dct.
            Called by Processor.build_params() """
        callnumber_dct = None
        params = { 'q': "callnumber_t:'%s'" % callnumber, 'wt': 'json', 'indent': 'true' }
        r = requests.get( self.SOLR_URL, params=params )
        log.debug( 'callnumber solr_url, `%s`' % r.url )
        raw_dct = json.loads( r.content )
        if raw_dct['response']['numFound'] > 0:
            doc = raw_dct['response']['docs'][0]
            author = doc.get( 'author_display', '' )
            callnumber_dct = { 'title': doc.get( 'title_display', '' ), 'author': author.split( ',' )[0] }
        log.debug( 'callnumber_dct, `%s`' % callnumber_dct )
        return callnumber_dct

    def run_query( self, params ):
        """ Runs solr query & returns json.
            Called by Processor.process_request() """
        r = requests.get( self.SOLR_URL, params=params )
        log.debug( 'full solr_url, `%s`' % r.url )
        utf8_content = r.content
        return utf8_content

    # end class SolrAccessor


class CatalogAccessor( object ):
    """ Handles catalog queries. """

    def __init__( self ):
        self.CATALOG_URL = 'https://search.library.brown.edu/catalog.json'
        self.standard_params = {
            'utf8': '✓',
            'op': 'AND',
            'f_inclusive[format][]': 'Book',
            'sort': 'score desc, pub_date_sort desc, title_sort asc',
            'search_field': 'advanced',
            'commit': 'Search',
            # 'title': 'The union of the oceans'
            # 'author': 'Kelley'
            }
