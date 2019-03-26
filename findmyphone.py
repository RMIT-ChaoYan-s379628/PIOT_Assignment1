
#!/usr/bin/env python3
import bluetooth
import sqlite3
import os
import time
import json
import sys
# from pushbullet import Pushbullet
from sense_hat import SenseHat

num = 0
read_file = open('config.json', "r")
data = json.load(read_file)
max_tem = data['max_temperature']
min_tem = data['min_temperature']
max_hum = data['max_humidity']
min_hum = data['min_humidity']
# pb = Pushbullet('o.p6OF0MXEo2huO3Ajf687fBUczZsTfvHV')

# Main function


def main():
    user_name = input("Enter your name: ")
    device_name = input("Enter the name of your phone: ")
    search(user_name, device_name)

# Search for device based on device's name


def search(user_name, device_name):
    conn = sqlite3.connect('sensehatTest.db')
    curs = conn.cursor()
    curs.execute(
        "CREATE TABLE IF NOT EXISTS BLUETOOTH_data(macAddress_Date STRING,count NUMERIC)")
    while True:
        device_address = None
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        time.sleep(3)  # Sleep three seconds
        nearby_devices = bluetooth.discover_devices()

        for mac_address in nearby_devices:
            if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                device_address = mac_address
                break
        if device_address is not None:
            print("Hi {}! Your phone ({}) has the MAC address: {}".format(
                user_name, device_name, device_address))
            sense = SenseHat()
            temp = round(sense.get_temperature(), 1)
            humi = round(sense.get_humidity(), 1)
            sense.clear()
            sense.show_message(
                "Hi {}! Current Temp is {}*c and current Humi is {}".format(user_name, temp, humi), scroll_speed=0.05)
            date = time.strftime("%a, %d %b %y", time.localtime())
            mac_address_date = date+mac_address
            curs.execute(
                "REPLACE INTO BLUETOOTH_data VALUES ((?),(0));", (mac_address_date,))
            if (temp <= max_tem and temp >= min_tem and humi <= max_hum and humi >= min_hum):
                curs.execute(
                    "select * from BLUETOOTH_data where macAddress_Date=(?);", (mac_address_date,))
                for row in curs.fetchall():
                    if row[1] == 0:
                        print(1)
                       # push = pb.push_note(
                        #    "This is the title", "This is the body")
                        curs.execute(
                            "update BLUETOOTH_data set count=1 where macAddress_Date=(?);", (mac_address_date,))
            conn.commit()
        else:
            print("Could not find target device nearby...")


# Execute program
main()
