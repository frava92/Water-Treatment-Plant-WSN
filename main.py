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

import time
import serial
from datetime import datetime
import XBee

dir_OD = 0x0E01
dir_ORP = 0X0E04
frame_OPT = 0x00
frame_ID = 0x01
req_DATA = (bytearray.fromhex("41 3C"))


#Initializar xbee port
xbee = XBee.XBee("/dev/ttyUSB5")
msg = 0
#Send Data Request for OD and wait for the response
xbee.Send(req_DATA,dir_OD,frame_OPT,frame_ID)
while msg == 0:
	frame = xbee.Receive()
	if frame != None:
		msg = 1	
		time.sleep(0.25)
		year = datetime.now().year
		month = datetime.now().month
		day = datetime.now().day
		hour = datetime.now().hour
		minute = datetime.now().minute
		second = datetime.now().second
		data_OD = frame[7:-1]
		print xbee.format(data_OD)
xbee.Send(req_DATA,dir_ORP,frame_OPT,frame_ID)
msg = 0
while msg == 0:
	frame = xbee.Receive()
	if frame != None:
		msg = 1	
		time.sleep(0.25)
		year = datetime.now().year
		month = datetime.now().month
		day = datetime.now().day
		hour = datetime.now().hour
		minute = datetime.now().minute
		second = datetime.now().second
		data_ORP = frame[7:-1]
		print xbee.format(data_ORP)
		
file = open("/var/spool/sms/outgoing/text","w")
file.write("To: 50688393752\n")
file.write("\n")
file.write("ORP: %s OD: %s" % (xbee.format(data_ORP), xbee.format(data_OD)))
