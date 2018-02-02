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

from lib.ptarlib import *


dir_OD = 0x0E01
xbee = XBee.XBee("/dev/ttyUSB0")
database = './db/PTAR_Residencial_Belen.db'

#from signal import signal, SIGPIPE, SIG_IGN
#signal(SIGPIPE,SIG_IGN)

def main():
	data_OD = request_data
	conn = connect_db(database)
	db_insert(conn, data_OD)
	if data_OD < 1.5 or data_OD > 4.0:
		send_alert

if __name__ == '__main__':
    main()





#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)
