#!/usr/bin/env python
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

import time
import serial
from datetime import datetime
import Xbee

dir_OD = 0x0E01
dir_ORP = 0X0E04
frame_OPT = 0x00
frame_ID = 0x01
reg_DATA = bytearray.fromhex("C1 3C")


def main(args):
    return 0

if __name__ == '__main__':
    import sys
	
	#Initializar xbee port
    xbee = XBee.XBee("/dev/ttyUSB0")
	msg = 0
	
	#Send Data Request for OD and wait for the response
	#requestData()
	xbee.Send(req_DATA,dir_OD,frame_OPT,frame_ID)
	while msg == 0
		frame = xbee.Receive()
		if frame != None:
			msg = 1	
			sleep(0.25)
			year = datetime.now().year
			month = datetime.now().month
			day = datetime.now().day
			hour = datetime.now().hour
			minute = datetime.now().minute
			second = datetime.now().second
			data_OD = frame[7:-1]
	
	xbee.Send(req_DATA,dir_ORP,frame_OPT,frame_ID)
	while msg == 0
		frame = xbee.Receive()
		if frame != None:
			msg = 1	
			sleep(0.25)
			year = datetime.now().year
			month = datetime.now().month
			day = datetime.now().day
			hour = datetime.now().hour
			minute = datetime.now().minute
			second = datetime.now().second
			data_ORP = frame[7:-1]
			

	conn = sqlite3.connect('./db/PTAR_Residencial_Belen.db')
	with conn:
		cur=conn.cursor()
		cur.execute("INSERT INTO mediciones values(?,?,?,?,?);", (id, date, time, data_OD, data_ORP))
		#cur.execute("INSERT INTO mediciones values(?, ?, ?, ?, ?, ?, ?, ?);", (counter, year, month, day, hour, minute, second, data_OD))
	
    sys.exit(main(sys.argv))