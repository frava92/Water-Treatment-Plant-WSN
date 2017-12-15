#! /usr/bin/env python

from datetime import datetime, date, timedelta
import sqlite3
import pandas as pd

#def send_summary():
def main():
    conn = sqlite3.connect('./db/PTAR_Residencial_Belen.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    #Fetching dates
    tomorrow =  datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')
    today = datetime.now().date()

    #Selecting all table data to extract column names
    cur.execute("select * from temps;")
    columns = cur.fetchone()

    #Extracting today's data
    cur.execute("select * from temps where timestamp between ? and ?;",(today,tomorrow))
    today_data = cur.fetchall()

    df=pd.DataFrame(todaysData)
    df.columns = columns.keys()
    print(df)

if __name__ == '__main__':
    main()
