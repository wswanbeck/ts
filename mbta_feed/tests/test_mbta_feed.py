#!/usr/bin/env python
# encoding: utf-8

import unittest

import __add_path
__add_path.add_path('../..')

from mbta_feed.mbta_feed import MbtaFeed
from db.mbta_status_sqlite import MbtaStatus_sqlite

class TestMbtaFeed(unittest.TestCase):

    def test1(self):
        m = MbtaFeed(MbtaStatus_sqlite("mbta_feed_unittest.sqlite"))
        m.read_feeds()
        m.save_data()

if __name__ == '__main__':
        unittest.main()
