#! /usr/bin/env python

from datetime import datetime, date, timedelta
import sqlite3
import pandas as pd

#def generate_summary():
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

    #Generating Data Frame
    df=pd.DataFrame(todaysData)
    df.columns = columns.keys()

    #Generating report_file
    path = "../reports/" #Path to report_file
    name = "Residencial_Belen" + str(datetime.now().date()) + ".xlsx" #name for the report_file
    report_name = path+name
    writer = pd.ExcelWriter(report_name)
    df.to_excel(writer,'Sheet1')
    writer.close()

def prep_mail():
    report_template = read_template('report.txt')




if __name__ == '__main__':
    main()
