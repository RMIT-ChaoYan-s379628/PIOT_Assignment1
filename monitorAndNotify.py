#!/usr/bin/env python3
import time
import json
import sqlite3
import sys
import requests
from sense_hat import SenseHat

read_file = open('config.json', "r")
data = json.load(read_file)
max_tem = data['max_temperature']
min_tem = data['min_temperature']
max_hum = data['max_humidity']
min_hum = data['min_humidity']
ACCESS_TOKEN = "o.p6OF0MXEo2huO3Ajf687fBUczZsTfvHV"

# get data from SenseHat sensor


def getSenseHatData():
    sense = SenseHat()
    temp = sense.get_temperature()
    humi = sense.get_humidity()
    if temp is not None and humi is not None:
        temp = round(temp, 1)
        humi = round(humi, 1)
        logData(temp, humi)

# log sensor data on database


def logData(temp, humi):
    conn = sqlite3.connect('sensehat.db')
    curs = conn.cursor()
    sql_createTB = '''CREATE TABLE IF NOT EXISTS SENSEHAT_data
    (timestamp DATETIME, temp NUMERIC,humi NUMERIC)'''
    curs.execute(sql_createTB)
    sql_insertData = '''INSERT INTO SENSEHAT_data values
    (datetime('now','localtime'), (?),(?))'''
    curs.execute(sql_insertData, (temp, humi,))
    conn.commit()
    conn.close()
    notify(temp, humi)

# notify the unexpected temperature and humidity to user with the Pushbullet


def notify(temp, humi):
    conn = sqlite3.connect('sensehat.db')
    curs = conn.cursor()
    sql_notify_createTB = '''CREATE TABLE IF NOT EXISTS NOTIFICATION_data
    (timestamp DATETIME, count NUMERIC)'''
    curs.execute(sql_notify_createTB)
    sql_notify_insertData = '''INSERT INTO NOTIFICATION_data ( timestamp, count )
    SELECT * FROM( SELECT date( 'now','localtime' ), 0 ) AS tmp
    WHERE NOT EXISTS (SELECT timestamp FROM NOTIFICATION_data
    WHERE timestamp = date( 'now','localtime' ) ) LIMIT 1; '''
    curs.execute(sql_notify_insertData)
    sql_update = '''update NOTIFICATION_data set count=1
    where timestamp=date('now','localtime');'''
    if (temp > max_tem or temp < min_tem or humi > max_hum or humi < min_hum):
        sql_select = '''select count from NOTIFICATION_data
        where timestamp=date('now','localtime');'''
        curs.execute(sql_select)
        for row in curs.fetchall():
            if row[0] == 0:
                print("ok")
                send_notification_via_pushbullet(
                    "Notification from Raspberry: ",
                    "The data is out of range.")
                curs.execute(sql_update)
            else:
                curs.execute(sql_update)
    conn.commit()
    conn.close()

# notify message to user via the Pushbullet


def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}

    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')

# main function


def main():
    getSenseHatData()


# Execute program
main()
