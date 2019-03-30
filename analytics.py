#!/usr/bin/env python3
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import pandas as pd
from dateutil.parser import parse
import pygal


x_ticks = []
y_temp = []
x = []


def check(count):
    conn = sqlite3.connect('sensehat.db')
    curs = conn.cursor()
    y = []
    curs.execute(
        "select count(1) from SENSEHAT_data; ")
    count_num = curs.fetchone()[0]
    print(count_num)
    curs.execute(
        "select timestamp,humi,temp from SENSEHAT_data; ")

    for index, row in enumerate(curs.fetchall()):
        if index+1 == count_num/15:

            break
        x .append(row[0])
        y .append(row[1])
        y_temp.append(row[2])
        if index % 5 == 0:
            x_ticks.append(row[0])

    print(x_ticks)
    print("print humidity")
    fig1 = plt.figure(figsize=(20, 10))
    ax1 = fig1.add_subplot(1, 1, 1)
    ax1.xaxis.set_major_formatter(mdate.DateFormatter(
        '%Y-%m-%d %H:%M:%S'))  # set time format
    print(x[0])
    a = parse(x[0])
    b = parse(x[len(x)-1])
    the_diff = (a-b).total_seconds()
    init_div = 180
    # calculate change
    while True:
        if the_diff % init_div == 0:
            break
        else:
            init_div = init_div-1

    print(len(x))

    print(len(y))
    print(pd.date_range(start=x[0], end=x[len(x)-1],
                        freq=str(init_div)+'s', normalize=False))
    print(x)
    print(y)
    ax1.set_xticks(range(len(x)))
    ax1.set_xticklabels(x, rotation=90)
    plt.title("The Humidity Graph", fontsize=20)
    plt.xlabel("DateTime", fontsize=20)
    plt.ylabel("Humidity(%)", fontsize=20)
    plt.plot(x, y)
    plt.savefig('Humidity.png')
    print("Finish humidity figure")
    date_chart = pygal.Line(x_label_rotation=90)
    date_chart.title = "The Temperature Graph"
    date_chart.x_labels = x
    date_chart.add("Temperature(℃)", y_temp)
    date_chart.render_to_file('bar_chart.svg')


# run the function
check(10)
