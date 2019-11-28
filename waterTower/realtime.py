import sqlite3
import time 

db = sqlite3.connect('file:swat_s1_db.sqlite?mode=ro', uri=True)

cursorObj = db.cursor()

while True:
    cursorObj.execute('SELECT name, value FROM swat_s1 WHERE name="LIT101"')
    row = cursorObj.fetchall()

    print(row[0][1])
    time.sleep(0.5)