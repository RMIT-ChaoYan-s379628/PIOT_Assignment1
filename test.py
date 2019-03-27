#!/usr/bin/env python3
import sqlite3
import os
import time
import sys

testvar = 0


def search():
    conn = sqlite3.connect('sensehatTest.db')
    curs = conn.cursor()
    curs.execute(
        "CREATE TABLE IF NOT EXISTS BLUETOOTH_data(macAddress_Date STRING PRIMARY KEY,count NUMERIC)")
    dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
    print("\nCurrently: {}".format(dt))
    time.sleep(3)  # Sleep three seconds
    date = time.strftime("%a, %d %b %y", time.localtime())
    print (date)
    mac_address_date = date
    print (mac_address_date)
    # sql = '''INSERT INTO BLUETOOTH_data ( macAddress_Date, count )
    # SELECT * FROM( SELECT (?), 0 ) AS tmp
    # WHERE NOT EXISTS (SELECT macAddress_Date FROM BLUETOOTH_data
    # WHERE macAddress_Date = (?)) LIMIT 1; '''
    curs.execute("INSERT OR IGNORE INTO BLUETOOTH_data VALUES ((?),0)",(mac_address_date,))
    conn.commit()
    if (testvar < 10):
        curs.execute(
            "select count from BLUETOOTH_data where macAddress_Date=(?);", (mac_address_date,))
        for row in curs.fetchall():
            if row[0] == 0:
                print(1)
                # push = pb.push_note(
                #    "This is the title", "This is the body")
            curs.execute(
                "update BLUETOOTH_data set count=1 where macAddress_Date=(?);", (mac_address_date,))
        conn.commit()

while True:
    search()