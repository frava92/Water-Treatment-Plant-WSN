#! /usr/bin/env python

from datetime import datetime, date, timedelta
import sqlite3
import pandas as pd

#def send_summary():
def main():
    conn = sqlite3.connect('./db/PTAR_Residencial_Belen.db')
    cur _ conn.cursor()
    tomorrow =  datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')
    today = datetime.now().date()
    cur.execute("select * from table where timestamp between ? and ?",(today,tomorrow)
    todays_data = cur.fetchall()
    print pd.read_sql_query(todays_data)
    for row in todays_data:
      print(row)

if __name__ == '__main__':
    main()
