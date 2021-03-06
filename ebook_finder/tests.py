# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from ebook_finder.models import Processor
# from ebook_finder.models import SolrAccessor
# from ebook_finder.tests import SolrData

# slr = SolrAccessor()
# solr_data = SolrData()


class ProcessorTest( TestCase ):
    """ Tests models.Processor() """

    def setUp( self ):
        self.slr_data = SolrData()
        self.processor = Processor()

    def test_massage_data__author_title_A( self ):
        """ Checks parse of solr response. """
        dct_resp = self.slr_data.author_title_response_A
        self.assertEqual(
            [{u'author': u'Mu\xf1oz, Jos\xe9 Esteban',
              u'bib': u'b7779467',
              u'language': [u'English'],
              u'pub_date': [u'2009'],
              u'title': u'Cruising utopia the then and there of queer futurity',
              u'url': u'https://login.revproxy.brown.edu/login?url=http://site.ebrary.com/lib/brown/Doc?id=10425196'}],
            self.processor.massage_data( verbosity='full', raw_data_dct=dct_resp )
            )

    def test_massage_data__author_title_B( self ):
        """ Checks parse of solr response. """
        dct_resp = self.slr_data.author_title_response_B
        self.assertEqual(
            [{u'author': u'Bald, Vivek',
              u'bib': u'b7119857',
              u'language': [u'English'],
              u'pub_date': [u'2013'],
              u'title': u'Bengali Harlem and the lost histories of South Asian America',
              u'url': u'https://login.revproxy.brown.edu/login?url=http://site.ebrary.com/lib/brown/Doc?id=10642232'},
             {u'author': u'Bald, Vivek',
              u'bib': u'b7154298',
              u'language': [u'English'],
              u'pub_date': [u'2012'],
              u'title': u'Bengali Harlem and the lost histories of South Asian America',
              u'url': u'https://login.revproxy.brown.edu/login?url=http://search.ebscohost.com/login.aspx?direct=true&scope=site&db=e000xna&AN=502790'}],
            self.processor.massage_data( verbosity='full', raw_data_dct=dct_resp )
            )

# class SolrAccessorTest( TestCase ):
#     """ Tests models.SolrAccessor() """

#     def test__check_title( self ):
#         """ Tests title solr query.
#             Not implemented due to solr being locked-down. """
#         title = 'Zen-brain horizons : toward a living zen'
#         title_params = slr.build_title_params( title )
#         utf8_jsn = slr.run_query( title_params )
#         self.assertEqual(
#             'foo',
#             utf8_jsn
#             )


class SolrData( object ):
    """ Holds data for testing. """

    def __init__( self ):
        self.author_title_response_A = {
             u'facet_counts': {u'facet_dates': {},
              u'facet_fields': {u'format': [u'Book', 1],
               u'language_facet': [u'English', 1],
               u'lc_1letter_facet': [],
               u'lc_alpha_facet': [],
               u'lc_b4cutter_facet': [],
               u'pub_date': [u'2009', 1],
               u'subject_era_facet': [],
               u'subject_geo_facet': [],
               u'subject_topic_facet': []},
              u'facet_queries': {},
              u'facet_ranges': {}},
             u'response': {u'docs': [{u'author_display': u'Mu\xf1oz, Jos\xe9 Esteban',
                u'format': u'Book',
                u'id': u'b7779467',
                u'isbn_t': [u'9780814757277 (cl : alk. paper)',
                 u'0814757278 (cl : alk. paper)',
                 u'9780814757284 (pb : alk. paper)',
                 u'0814757286 (pb : alk. paper)'],
                u'language_facet': [u'English'],
                u'pub_date': [u'2009'],
                u'published_display': [u'New York'],
                u'score': 12.99476,
                u'title_display': u'Cruising utopia the then and there of queer futurity',
                u'url_fulltext_display': [u'https://login.revproxy.brown.edu/login?url=http://site.ebrary.com/lib/brown/Doc?id=10425196'],
                u'url_suppl_display': [u'Full text available from Ebrary Academic Complete Subscription Collection']}],
              u'maxScore': 12.99476,
              u'numFound': 1,
              u'start': 0},
             u'responseHeader': {u'QTime': 13,
              u'params': {u'defType': u'lucene',
               u'f.author_facet.facet.limit': u'21',
               u'fq': [u'{!raw f=format}Book', u'access_facet:("Online")'],
               u'indent': u'true',
               u'q': u'_query_:"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}Cruising utopia" AND _query_:"{!dismax spellcheck.dictionary=author qf=$author_qf pf=$author_pf}Munoz"',
               u'rows': u'10',
               u'sort': u'score desc, pub_date_sort desc, title_sort asc',
               u'wt': u'json'},
              u'status': 0}}
        self.author_title_response_B = {
             u'facet_counts': {u'facet_dates': {},
              u'facet_fields': {u'format': [u'Book', 3],
               u'language_facet': [u'English', 3],
               u'lc_1letter_facet': [],
               u'lc_alpha_facet': [],
               u'lc_b4cutter_facet': [],
               u'pub_date': [u'2013', 2, u'2012', 1],
               u'subject_era_facet': [],
               u'subject_geo_facet': [],
               u'subject_topic_facet': []},
              u'facet_queries': {},
              u'facet_ranges': {}},
             u'response': {u'docs': [{u'author_display': u'Bald, Vivek',
                u'format': u'Book',
                u'id': u'b6284150',
                u'isbn_t': [u'9780674066663',
                 u'0674066669',
                 u'9780674067578 (ebook)',
                 u'0674067576 (ebook)'],
                u'language_facet': [u'English'],
                u'pub_date': [u'2013'],
                u'score': 25.486412,
                u'title_display': u'Bengali Harlem and the lost histories of South Asian America'},
               {u'author_display': u'Bald, Vivek',
                u'format': u'Book',
                u'id': u'b7119857',
                u'isbn_t': [u'9780674066663',
                 u'0674066669',
                 u'9780674067578 (ebook)',
                 u'0674067576 (ebook)'],
                u'language_facet': [u'English'],
                u'pub_date': [u'2013'],
                u'published_display': [u'Cambridge, Mass'],
                u'score': 25.486412,
                u'title_display': u'Bengali Harlem and the lost histories of South Asian America',
                u'url_fulltext_display': [u'https://login.revproxy.brown.edu/login?url=http://site.ebrary.com/lib/brown/Doc?id=10642232'],
                u'url_suppl_display': [u'Full text available from Ebrary Academic Complete Subscription Collection']},
               {u'author_display': u'Bald, Vivek',
                u'format': u'Book',
                u'id': u'b7154298',
                u'isbn_t': [u'9780674067578 (electronic bk.)',
                 u'0674067576 (electronic bk.)',
                 u'9780674066663',
                 u'0674066669'],
                u'language_facet': [u'English'],
                u'pub_date': [u'2012'],
                u'published_display': [u'Cambridge, Mass'],
                u'score': 25.486412,
                u'title_display': u'Bengali Harlem and the lost histories of South Asian America',
                u'url_fulltext_display': [u'https://login.revproxy.brown.edu/login?url=http://search.ebscohost.com/login.aspx?direct=true&scope=site&db=e000xna&AN=502790'],
                u'url_suppl_display': [u'Full text available from EBSCO eBook Academic Subscription Collection']}],
              u'maxScore': 25.486412,
              u'numFound': 3,
              u'start': 0},
             u'responseHeader': {u'QTime': 24,
              u'params': {u'defType': u'lucene',
               u'f.author_facet.facet.limit': u'21',
               u'fq': [u'{!raw f=format}Book', u'access_facet:("Online")'],
               u'indent': u'true',
               u'q': u'_query_:"{!dismax spellcheck.dictionary=title qf=$title_qf pf=$title_pf}Bengali Harlem and the lost histories of South Asian America" AND _query_:"{!dismax spellcheck.dictionary=author qf=$author_qf pf=$author_pf}Bald, Vivek"',
               u'rows': u'10',
               u'sort': u'score desc, pub_date_sort desc, title_sort asc',
               u'wt': u'json'},
              u'status': 0}}

    # end class SolrData()
