import XBee
from time import sleep

if __name__ == "__main__":
    xbee = XBee.XBee("/dev/ttyUSB0")  # Your serial port name here

    # A simple string message
    #sent = xbee.SendStr("Hello World")
    #sleep(0.25)
    #Msg = xbee.Receive()
    #if Msg:
    #    content = Msg[7:-1].decode('ascii')
    #    print("Msg: " + content)

    # A message that requires escaping
    #xbee.Send(bytearray.fromhex("C1 3C"),0x0E04,0x00,0x01)
    while 1:
		sleep(1)
		#frame = 1
		frame = xbee.Receive()
		if frame != None:
			content = frame[7:-1]
			print xbee.format(content)
			#print frame
