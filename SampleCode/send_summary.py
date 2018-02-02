#! /usr/bin/env python

from datetime import datetime, date, timedelta
import sqlite3
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

MY_ADDRESS = 'fvargas9201@gmail.com'
PASSWORD = 'FraVarAcu1992'
EMAIL = "franzvargas91@gmail.com"

def main():
    generate_summary
    send_summary

def generate_summary():
    conn = sqlite3.connect('./db/PTAR_Residencial_Belen.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    #Fetching dates
    tomorrow =  datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')
    today = datetime.now().date()

    #Selecting all table data to extract column names
    cur.execute("select * from mediciones;")
    columns = cur.fetchone()

    #Extracting today's data
    cur.execute("select * from mediciones where date between ? and ?;",(today,tomorrow))
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

def send_summary():

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    msg['From']="PTAR Residencial Belen"
    msg['To']=EMAIL
    msg['Subject']="Status"

    body = "Buenas tardes, adjunto se encuentra el status del dia"
    msg.attach(MIMEText(body, 'plain'))

    filename = "PTAR.Belen_" + str(datetime.now().date()) + ".xlsx"
    attachment = open("./reports/"+filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)
    text = msg.as_string()
    s.sendmail(MY_ADDRESS, EMAIL, text)
    del msg
    s.quit()




if __name__ == '__main__':
    main()
