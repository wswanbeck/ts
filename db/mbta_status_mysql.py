#!/usr/bin/env python
# encoding: utf-8

try:
    import MySQLdb
except:
    pass
import time
import datetime

from utils.utils import Utils


class MbtaStatus_msql:

    def __init__(self, dbhost, dbuser, dbpassword, dbname):
        self.conn = None
        self.cur = None
        self.dbhost = dbhost
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbname = dbname

        self.__enter__()

    def __enter__(self):
        self._connect()
        return self

    def _connect(self):
        # connect to db if we haven't already connected to it
        if not self.conn:
            #self.conn=MySQLdb.connect(host="mysql.trainstats.swanbeck.net", user="trainstats", passwd="trainstats1", db="trainstats")
            self.conn=MySQLdb.connect(host=self.dbhost, user=self.dbuser, passwd=self.dbpassword, db=self.dbname)
            self.cur = self.conn.cursor()
            self.cur.execute('CREATE TABLE if not exists VEHICLES (trip text, date text, day text, time text, vehicle text, primary key (trip, date)) ')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()

    def _disconnect(self):
        # disconnect from database if we haven't already disconnected from it
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = self.cur = None

    def add_status_entry(self, trip, t, vehicle):
        self._connect()
        dd = datetime.date.fromtimestamp(time.time())
        self.cur.execute('INSERT or REPLACE INTO VEHICLES (trip, date, day, time, vehicle) values (?, ?, ?, ?, ?)',
              [trip, dd.strftime('%Y %b %d'), dd.strftime('%a'), t, vehicle])
        self.conn.commit()

    def get_likely_vehicles(self, nexttrip):
        prevtrips = []

        self._connect()
        self.cur.execute('SELECT date, vehicle FROM VEHICLES where trip=? ORDER BY date DESC', [nexttrip])
        date_vehicles = self.cur.fetchall()

        for d, v in date_vehicles:
            self.cur.execute('SELECT trip FROM VEHICLES where date=? and vehicle=? order by time asc', [d, v])
            ts = self.cur.fetchall()
            if len(ts)> 1:
                # find the trip just before our trip
                prevtrip = None
                for triplist in ts:
                    trip = triplist[0]
                    if trip == nexttrip:
                        # previous trip (if any) led to this one
                        if prevtrip:
                            prevtrips.append(prevtrip)
                    else:
                        prevtrip = trip

        ranked_prev_trips = Utils.ranklist(prevtrips)

        vehicles = []
        for trip, count in ranked_prev_trips:
            # get the latest vehicle for each trip
            self.cur.execute('SELECT vehicle FROM VEHICLES where trip=? ORDER BY date DESC', [trip])
            vehicle = self.cur.fetchone()
            vehicles.append((vehicle, count))

        return vehicles

