import time
import json
import sqlite3
import sys
from pushbullet import Pushbullet
from sense_hat import SenseHat

read_file = open('config.json', "r")
data = json.load(read_file)
max_tem = data['max_temperature']
min_tem = data['min_temperature']
max_hum = data['max_humidity']
min_hum = data['min_humidity']

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
   # print(temp)
   # print(humi)
    curs.execute(
        "CREATE TABLE IF NOT EXISTS SENSEHAT_data(timestamp DATETIME, temp NUMERIC,humi NUMERIC)")
    curs.execute(
        "INSERT INTO SENSEHAT_data values(datetime('now','localtime'), (?),(?))", (temp, humi,))
    conn.commit()
    conn.close()
    notify(temp,humi)


def notify(temp, humi):
    pb = Pushbullet('o.p6OF0MXEo2huO3Ajf687fBUczZsTfvHV')
    conn = sqlite3.connect('sensehat.db')
    curs = conn.cursor()
    curs.execute(
        "CREATE TABLE IF NOT EXISTS NOTIFICATION_data(timestamp DATETIME, count NUMERIC)")
    curs.execute(
        "INSERT INTO NOTIFICATION_data ( timestamp, count ) SELECT * FROM( SELECT date( 'now','localtime' ), 0 ) AS tmp WHERE NOT EXISTS (SELECT timestamp FROM NOTIFICATION_data WHERE timestamp = date( 'now','localtime' ) ) LIMIT 1; ")
    if (temp>max_tem or temp<min_tem or humi>max_hum or humi<min_hum):
        curs.execute(
            "select count from NOTIFICATION_data where timestamp=date('now','localtime');")
        for row in curs.fetchall():
            if row[0] == 0:
                print("ok")
                pb = Pushbullet('o.p6OF0MXEo2huO3Ajf687fBUczZsTfvHV')
                pb.push_note("Notification from Raspberry", "The data is out of range.")
                curs.execute(
                "update NOTIFICATION_data set count=1 where timestamp=date('now','localtime');")
            else:
                curs.execute(
                "update NOTIFICATION_data set count=1 where timestamp=date('now','localtime');")
    conn.commit()
    conn.close()


# main function
def main():
    getSenseHatData()


# Execute program
main()
