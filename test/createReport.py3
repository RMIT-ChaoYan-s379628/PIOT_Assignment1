import csv
import json
import sqlite3

read_file = open('config.json', "r")
data = json.load(read_file)
max_tem = data['max_temperature']
min_tem = data['min_temperature']
max_hum = data['max_humidity']
min_hum = data['min_humidity']

with open('report.csv', 'w') as csvfile:
    fieldnames = ['Data', 'Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    conn = sqlite3.connect('sensehat.db')
    cur = conn.cursor()
    cur.execute("select strftime('%Y-%m-%d',timestamp) as date ,AVG(temp) as average from SENSEHAT_data group by strftime('%Y-%m-%d', timestamp);")
    writer.writeheader()
    for row in cur.fetchall():
        if row[1] <= max_tem and row[1] >= min_tem:
            writer.writerow({'Data': row[0], 'Status': "OK"})
        elif row[1] > max_tem:
            result = round(abs(row[1]-max_tem), 1)
            writer.writerow({'Data': row[0], 'Status': repr(
                result)+"*c above the maximum temperature."})
        elif row[1] < min_tem:
            result = round(abs(row[1]-min_tem), 1)
            writer.writerow({'Data': row[0], 'Status': repr(
                result)+"*c below the maximum temperature."})
