import sqlite3
conn=sqlite3.connect('sensehat.db')
cur=conn.cursor()
#print(cur.execute("select AVG(temp) as total from SENSEHAT_data"))
for row in cur.execute("select AVG(temp) as total from SENSEHAT_data"):
        print (row)