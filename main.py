#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
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

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    xbee = XBee.XBee("/dev/ttyUSB0")
    Msg = xbee.Receive()
    if Msg:
		year = datetime.now().year
		month = datetime.now().month
		day = datetime.now().day
		hour = datetime.now().hour
		minute = datetime.now().minute
		second = datetime.now().second
		
		conn = sqlite3.connect('./db/PTAR_Residencial_Belen.db')
		with conn:
			cur=conn.cursor()
			cur.execute("INSERT INTO mediciones values(?, ?, ?, ?, ?, ?, ?, ?);", (counter, year, month, day, hour, minute, second, DATA))
	
    sys.exit(main(sys.argv))
