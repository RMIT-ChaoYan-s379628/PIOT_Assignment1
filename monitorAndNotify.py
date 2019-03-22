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
    print(temp)
    print(humi)
    curs.execute(
        "CREATE TABLE IF NOT EXISTS SENSEHAT_data(timestamp DATETIME, temp NUMERIC,humi NUMERIC)")
    curs.execute(
        "INSERT INTO SENSEHAT_data values(datetime('now'), (?),(?))", (temp, humi,))
    conn.commit()
    conn.close()


def notify(temp, humi):
    pb = Pushbullet('o.p6OF0MXEo2huO3Ajf687fBUczZsTfvHV')
    conn = sqlite3.connect('sensehat.db')
    curs = conn.cursor()
    curs.execute(
        "CREATE TABLE IF NOT EXISTS NOTIFICATION_data(timestamp DATETIME, count NUMERIC)")
    curs.execute(
        "INSERT INTO SENSEHAT_data values(date('now'), (0)")
    if (temp>max_tem or temp<min_tem or humi>max_hum or humi<min_hum):
        curs.execute("select * from NOTIFICATION_data where timestamp=date('now');")
        for row in curs.fetchone():
            if row[1]==0 :
                push = pb.push_note("This is the title", "This is the body")
        curs.execute("update NOTIFICATION_data set count=1 where timestamp=date('now');")
    conn.commit()
    conn.close()


# main function
def main():
    getSenseHatData()


# Execute program
main()
