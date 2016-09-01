# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from ebook_finder.models import SolrAccessor


# slr = SolrAccessor()


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
