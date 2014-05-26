#!/usr/bin/env python
# encoding: utf-8

import unittest

import __add_path
from utils.utils import Utils

__add_path.add_path('../..')

from mbta_feed.mbta_feed import MbtaFeed
from db.mbta_status_sqlite import MbtaStatus_sqlite


class TestMbtaFeed(unittest.TestCase):

    def test_read_and_save(self):
        m = MbtaFeed(MbtaStatus_sqlite("mbta_feed_unittest.sqlite"))
        m.read_feeds()
        m.save_data()

    def test_find_vehicles(self):
        db = MbtaStatus_sqlite('mbta_feed_unittest_static.sqlite')
        vs = db.get_likely_vehicles('not-found')
        self.assertTrue(len(vs) == 0)
        vs = db.get_likely_vehicles('2406')
        self.assertTrue(len(vs) == 0)
        pass

    def test_utils(self):

        testlist = [1, 2, 3, 3, 4, 5, 1, 1, 1, 2]
        rankedlist = Utils.ranklist(testlist)
        self.assertEqual(rankedlist,
            [(1, 4), (2, 2), (3, 2), (4, 1), (5, 1)])
        pass


if __name__ == '__main__':
        unittest.main()
