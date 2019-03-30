#!/usr/bin/env python3
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
    sql = '''select strftime('%Y-%m-%d',timestamp) as date ,
           AVG(temp) as temp_average, AVG(humi) as humi_average
           from SENSEHAT_data group by strftime('%Y-%m-%d', timestamp);'''
    cur.execute(sql)
    writer.writeheader()
    for row in cur.fetchall():
        if row[1] <= max_tem and row[1] >= min_tem:
            if row[2] <= max_hum and row[2] >= min_hum:
                writer.writerow({'Data': row[0], 'Status': "OK"})
            elif row[2] > max_hum:
                result = round(abs(row[2]-max_hum), 1)
                writer.writerow({'Data': row[0], 'Status': repr(
                    result)+"% above the maximum humidiy."})
            elif row[2] < min_hum:
                result = round(abs(row[2]-min_hum), 1)
                writer.writerow({'Data': row[0], 'Status': repr(
                    result)+"% below the minimum humidiy."})
        elif row[1] > max_tem:
            result_tem = round(abs(row[1]-max_tem), 1)
            if row[2] <= max_hum and row[2] >= min_hum:
                writer.writerow({'Data': row[0], 'Status': repr(
                    result_tem)+"*c above the maximum temperature."})
            elif row[2] > max_hum:
                result_hum = round(abs(row[2]-max_hum), 1)
                writer.writerow({'Data': row[0], 'Status': repr(
                    result_tem)+"*c above the maximum temperature. "+repr(
                    result_hum)+"% above the maximum humidiy."})
            elif row[2] < min_hum:
                result_hum = round(abs(row[2]-min_hum), 1)
                writer.writerow({'Data': row[0], 'Status': repr(
                    result_tem)+"*c above the maximum temperature. "+repr(
                    result_hum)+"% below the minimum humidiy."})
        elif row[1] < min_tem:
            result_tem = round(abs(row[1]-min_tem), 1)
            if row[2] <= max_hum and row[2] >= min_hum:
                writer.writerow({'Data': row[0], 'Status': repr(
                    result_tem)+"*c below the minimum temperature."})
            elif row[2] > max_hum:
                result_hum = round(abs(row[2]-max_hum), 1)
                writer.writerow({'Data': row[0], 'Status': repr(
                    result_tem)+"*c below the minimum temperature. "+repr(
                    result_hum)+"% above the maximum humidiy."})
            elif row[2] < min_hum:
                result_hum = round(abs(row[2]-min_hum), 1)
                writer.writerow({'Data': row[0], 'Status': repr(
                    result_tem)+"*c below the minimum temperature. "+repr(
                    result_hum)+"% below the minimum humidiy."})
