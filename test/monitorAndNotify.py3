import time
import json
import sqlite3
import sys
from sense_hat import SenseHat

dbname='sensehat.db'
conn=sqlite3.connect(dbname)
with conn: 
    cur = conn.cursor() 
    # cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    cur.execute("CREATE TABLE IF NOT EXISTS SENSEHAT_data(timestamp DATETIME, temp NUMERIC)")

sampleFreq = 1 # time in seconds

# get data from SenseHat sensor
def getSenseHatData():	
    sense = SenseHat()
    temp = sense.get_temperature()
	
    if temp is not None:
        temp = round(temp, 1)
        logData (temp)

# log sensor data on database
def logData (temp):	
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO SENSEHAT_data values(datetime('now'), (?))", (temp,))
    conn.commit()
    conn.close()

# display database data
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM SenseHat_data"):
        print (row)
    conn.close()

# main function
def main():
    for i in range (0,60):
        getSenseHatData()
        time.sleep(sampleFreq)
    displayData()

# Execute program 
main()
