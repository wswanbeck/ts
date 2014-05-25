import urllib2
import json
import time



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

