#!/usr/bin/env python
# encoding: utf-8
import sqlite3
import time
import datetime


class MbtaStatus_sqlite:

    def __init__(self, dbname):
        self.conn = None
        self.cur = None
        self.dbname = dbname

        self.__enter__()

    def __enter__(self):
        self._connect()
        return self

    def _connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.dbname)
            self.cur = self.conn.cursor()
            self.cur.execute('CREATE TABLE if not exists VEHICLES (trip text, date text, time text, vehicle text, primary key (trip, date)) ')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()

    def _disconnect(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = self.cur = None

    def add_status_entry(self, trip, t, vehicle):
        self.cur.execute('INSERT or REPLACE INTO VEHICLES (trip, date, time, vehicle) values (?, ?, ?, ?)',
              [trip, datetime.date.fromtimestamp(time.time()).strftime('%a %Y %b %d'), t, vehicle])
        self.conn.commit()
