#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2017  <pi@raspberrypi>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import smtplib
from string import Template
from datetime import datetime, date, timedelta, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sqlite3
from sqlite3 import Error
import pandas as pd
import time
import serial
import XBee
import logging


dir_OD = 0x0E01
xbee = XBee.XBee("/dev/ttyUSB0")
database = './db/PTAR_Residencial_Belen.db'
MY_ADDRESS = 'fvargas9201@gmail.com'
PASSWORD = 'FraVarAcu1992'
EMAIL = "franzvargas91@gmail.com"


#from signal import signal, SIGPIPE, SIG_IGN
#signal(SIGPIPE,SIG_IGN)

def main():
	logging.basicConfig(format=('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	logging.info('Program started')
	conn = connect_db(database)
	logging.info('Successfully connected to database')
	logging.info('Requesting reading from sensor')
	data_OD = request_data
	logging.info('Successfully received reading from sensor')
	logging.info('Inserting data into database')
	db_insert(conn, data_OD)
	logging.info('Successfully inserted data into database')
	if data_OD < 1.5 or data_OD > 4.0:
		logging.info('')
		send_alert


def connect_db(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)

	return None

def db_insert(conn, data):
	currentDT = datetime.now()
	date_today = currentDT.strftime("%Y-%m-%d")
	time_now = currentDT.strftime("%H:%M:%S")
	with conn:
		cur = conn.cursor()
		cur.execute('INSERT INTO mediciones VALUES(?,?,?);',(date_today,time_now,data))

def send_alert():
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    msg['From']="PTAR Residencial Belen"
    msg['To']=EMAIL
    msg['Subject']="ALERT"

    body = "ALERTA: Niveles de OD fuera del rango permitido"
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    s.sendmail(MY_ADDRESS, EMAIL, text)
    del msg
    s.quit()

def request_data():
	msg = 0
	#Send Data Request for OD and wait for the response
	xbee.SendStr("R",dir_OD,0x00,0x01)
	while msg == 0:
		frame = xbee.Receive()
		if frame != None:
			msg = 1
			time.sleep(0.25)
			data_OD = frame[7:-1]
			return data_OD.decode('ascii')

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

def generate_summary(conn):
    #conn = sqlite3.connect('./db/PTAR_Residencial_Belen.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    #Fetching dates
    tomorrow =  datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')
    today = datetime.now().date()

    #Selecting all table data to extract column names
    cur.execute("select * from mediciones;")
    columns = cur.fetchone()

    #Extracting today's data
    cur.execute("select * from mediciones where timestamp between ? and ?;",(today,tomorrow))
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

if __name__ == '__main__':
    main()





#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)
