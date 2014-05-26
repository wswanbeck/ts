#!/usr/bin/env python
# encoding: utf-8
import urllib2
import json
import time
import datetime
import __add_path
__add_path.add_path('..')
from db.mbta_status_sqlite import MbtaStatus_sqlite


class MbtaFeed:

    feeds = ['http://developer.mbta.com/lib/RTCR/RailLine_9.json', # 9. Fitchburg
             'http://developer.mbta.com/lib/RTCR/RailLine_10.json', #10. Lowell
             'http://developer.mbta.com/lib/RTCR/RailLine_11.json', #11. Haverhill
             'http://developer.mbta.com/lib/RTCR/RailLine_12.json', #12. Newburyport/Rockport
             ]

    def __init__(self, db):
        # self.vehicles[trip] = [time added, vehicle]
        self.vehicles = dict()
        self.db = db

    def read_feeds(self):
        for feed in MbtaFeed.feeds:
            self.read_feed(feed)

    def read_feed(self, feed):
        req = urllib2.Request(feed)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        # let's hope that response.msg == 'OK' and response.code==200
        data = None
        if response.code == 200:
            data =  json.load(response)

        for message in data['Messages']:
            stop = message['Stop']
            dest = message['Destination']
            vehicle = message['Vehicle']
            trip = message['Trip']
            try:
                speed = int(message['Speed'])
            except:
                speed = 0

            flag = message['Flag']

            # vehicle is probably right if flag it not 'Pre' or 'Sch'
            if flag.lower() not in ['pre', 'sch']:
                self.save_vehicle(vehicle, trip)
                break
        pass

    def save_vehicle(self, vehicle, trip):
        self.vehicles[trip] = [time.time(), vehicle]

    def save_data(self):

        for trip in self.vehicles:
            [t, vehicle] = self.vehicles[trip]
            # if not already stored, then add it
            # if this entry has today's date, then update it
            # otherwise add a new entry
            self.db.add_status_entry(trip, t, vehicle)

        self.db._disconnect()


if __name__ == '__main__':
    print 'starting feed watch'
    m = MbtaFeed(MbtaStatus_sqlite("mbta_status.sqlite"))
    while True:
        print '%s: reading feed data' % (datetime.datetime.today().strftime('%H:%M'))
        m.read_feeds()
        print '  saving feed data'
        m.save_data()
        print '  sleeping for 15 minutes'
        time.sleep(60*15) # 15 minutes
