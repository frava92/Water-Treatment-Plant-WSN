import smtplib
from string import Template
from datetime import datetime, date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sqlite3
import pandas as pd
import XBee



MY_ADDRESS = 'fvargas9201@gmail.com'
PASSWORD = 'FraVarAcu1992'
EMAIL = "controloperacional@grupoproamsa.com"

def connect_db(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)

	return None

def db_insert(conn,data):
    with conn:
        cur = conn.cursor()
        cur. execute("INSERT INTO mediciones values(?,?);",(datetime.now(),data))

def send_alert():
	pass

def request_data():
	msg = 0
	#Send Data Request for OD and wait for the response
	xbee.Send(req_DATA,dir_OD,frame_OPT,frame_ID)
	while msg == 0:
		frame = xbee.Receive()
		if frame != None:
			msg = 1
			time.sleep(0.25)
			return xbee.format(data_OD)


def send_summary():

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    msg['From']="PTAR Residencial Belen"
    msg['To']=EMAIL
    msg['Subject']="Status"

    body = "Buenas tardes, adjunto se encuentra el status diario"
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
