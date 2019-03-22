import sqlite3
from pushbullet import Pushbullet


def check(count):
    conn = sqlite3.connect('sensehat.db')
    curs = conn.cursor()
    curs.execute(
        "CREATE TABLE IF NOT EXISTS NOTIFICATION_data(timestamp DATETIME, count NUMERIC)")
    curs.execute(
        "INSERT INTO NOTIFICATION_data ( timestamp, count ) SELECT * FROM( SELECT date( 'now' ), 0 ) AS tmp WHERE NOT EXISTS (SELECT timestamp FROM NOTIFICATION_data WHERE timestamp = date( 'now' ) ) LIMIT 1; ")
    if count > 5:
        curs.execute(
            "select count from NOTIFICATION_data where timestamp=date('now');")
        for row in curs.fetchall():
            if row[0] == 0:
                print("ok")
                pb = Pushbullet('o.p6OF0MXEo2huO3Ajf687fBUczZsTfvHV')
                pb.push_note("This is the title", "This is the body")
                curs.execute(
                "update NOTIFICATION_data set count=1 where timestamp=date('now');")
            else:
                curs.execute(
                "update NOTIFICATION_data set count=1 where timestamp=date('now');")
    conn.commit()
    conn.close()


check(10)
