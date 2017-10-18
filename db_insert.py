#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  serial_rx.py
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
                
import time
import serial
import sqlite3
import datetime
from datetime import datetime
import serial
          
ser = serial.Serial(
	port='/dev/ttyS0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5
)

conn = sqlite3.connect('./db/PTAR_Residencial_Belen.db')
counter = 1
while (counter < 10):
	year = datetime.now().year
	month = datetime.now().month
	day = datetime.now().day

	hour = datetime.now().hour
	minute = datetime.now().minute
	second = datetime.now().second
	
	OD = ser.readline()
	while OD == '':
		time.sleep(1)
		OD = ser.readline()
	with conn:
		cur = conn.cursor()
		cur.execute("INSERT INTO mediciones values(?, ?, ?, ?, ?, ?, ?, ?);", (counter, year, month, day, hour, minute, second, OD))
		#con.commit()
	print "Data inserted into DB"
	counter = counter + 1
	#time.sleep(2)
	

