import os
import RPI.GPIO as GPIO
from gps import *
from time import *
import time
import threading
GPIO.setmode(GPIO.BOARD)
GPIO.setup(24, GPIO.OUT)#GPS LOCK LED
gpsd = None #setting the global variable
class GpsPoller(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
        global gpsd #bring it in scope
        gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true
        def run(self):
                global gpsd
        while gpsp.running:
                gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
	if __name__ == '__main__':
        	gpsp = GpsPoller() # create the thread
        try:
                gpsp.start() # start it up
                while True:
                #It may take a second or two to get good data
                        print ' GPS mode:'
                        print '----------------------------------------'
                        print 'mode        ' , gpsd.fix.mode # all values greather than 1 is a GPS fix.
                while True:
			if gpsmode > 1:
				GPIO.output(24, True)
		if gpsmode < 1:
			GPIO.output(24, False)
