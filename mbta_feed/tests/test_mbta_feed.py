#!/usr/bin/env python
# encoding: utf-8

import unittest

import __add_path
__add_path.add_path('../..')

from mbta_feed.mbta_feed import MbtaFeed

class TestMbtaFeed(unittest.TestCase):

    def test1(self):
        m = MbtaFeed()
        m.read_feeds()

if __name__ == '__main__':
        unittest.main()
