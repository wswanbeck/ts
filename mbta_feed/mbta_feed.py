#!/usr/bin/env python
# encoding: utf-8
import urllib2
import json
import time
import datetime
import sqlite3


class MbtaFeed:

    feeds = ['http://developer.mbta.com/lib/RTCR/RailLine_9.json', # 9. Fitchburg
             'http://developer.mbta.com/lib/RTCR/RailLine_10.json', #10. Lowell
             'http://developer.mbta.com/lib/RTCR/RailLine_11.json', #11. Haverhill
             'http://developer.mbta.com/lib/RTCR/RailLine_12.json', #12. Newburyport/Rockport
             ]

    def __init__(self):
        # self.vehicles[trip] = [time added, vehicle]
        self.vehicles = dict()

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
        conn = sqlite3.connect('mbtadata.sqlite')
        cur = conn.cursor()
        cur.execute('CREATE TABLE if not exists VEHICLES (trip text, date text, time text, vehicle text, primary key (trip, date)) ')
        for trip in self.vehicles:
            [t, vehicle] = self.vehicles[trip]
            # if not already stored, then add it

            # get latest entry for this trip

            # if this entry has today's date, then update it

            # otherwise add a new entry
            cur.execute('INSERT or REPLACE INTO VEHICLES (trip, date, time, vehicle) values (?, ?, ?, ?)',
                  [trip, datetime.date.fromtimestamp(time.time()).strftime('%a %Y %b %d'), t, vehicle])
        conn.commit()
        conn.close()

if __name__ == '__main__':
    print 'starting feed watch'
    m = MbtaFeed()
    while True:
        print '%s: reading feed data' % (datetime.datetime.today().strftime('%H:%M'))
        m.read_feeds()
        print '  saving feed data'
        m.save_data()
        print '  sleeping for 15 minutes'
        time.sleep(60*15) # 15 minutes
