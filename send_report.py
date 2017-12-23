import time
import serial
import lib.XBee
from lib.ptarlib import *
import sqlite3
from sqlite3 import Error
from datetime import datetime
import smtplib
from string import Template
from datetime import datetime, date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sqlite3
import pandas as pd


def main():
	conn = connect_db(database)
	generate_report(conn)
	send_summary
