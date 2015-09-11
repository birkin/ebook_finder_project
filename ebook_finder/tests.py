# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase
from ebook_finder.models import SolrAccessor


slr = SolrAccessor()


class SolrAccessorTest( TestCase ):
    """ Tests models.SolrAccessor() """

    def test__check_title( self ):
        """ Tests title solr query. """
        self.assertEqual(
            'foo',
            slr.check_title( 'Zen-brain horizons : toward a living zen' )
            )
