import RPi.GPIO as GPIO
import os
import subprocess
import gps
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(04, GPIO.OUT)#LED1 KISMET
GPIO.setup(17, GPIO.OUT)#LED2 GPSD running
GPIO.setup(9, GPIO.OUT)#LED5 Upload in progress.
GPIO.setup(26, GPIO.IN)#Data upload switch,momentarily toggle.
GPIO.output(04, True)#Makes sure all LED's are at the same state initially (off):
GPIO.output(17, True)
GPIO.output(22, True)
GPIO.output(9, True)
GPIO.output(10, True)
while 1 < 2:
    kismet = subprocess.Popen(['ps -ef | grep kismet'],
    stdout=subprocess.PIPE, shell=True) #Assigns the output from the grep to the kismet variable
    (output, error) = kismet.communicate()
    if 'kismet_server' in output:
        GPIO.output(04, False) #Turn on KISMET LED
    else:
        GPIO.output(04, True) #Turn off KISMET LED
    gps = subprocess.Popen(['ps -ef | grep gpsd'],
    stdout=subprocess.PIPE, shell=True)#Assigns the output from the grepto the gps variable
    (output, error) = gps.communicate()
    if 'gpsd' in output:
        GPIO.output(17, False) #Turn on GPSD LED
    else:
        GPIO.output(17, True) #Turn off GPSD LED
    while True:
        if (GPIO.input(26)): #If upload button is pressed
            time.sleep(0.05)
            os.system("killall kismet")
            time.sleep(3)# added so kismet has the time to die.
            os.system("iwconfig wlan0 essid YOUR_NETWORK_ID key YOUR_WIRELESS_PASSWORD")
            time.sleep(10)# added so wlan0 has time to autenticate and assosiate with the wlan node
            GPIO.output(9, False)#Turns on LED5
            if connectivityTest(): #Checks for internet connectivity. (Mainly connectivity to wigle.net)
                print "This executes when there is connectivity to wigle.net"
            else:
                print "This executes when there is no connectivity to wigle.net"
    #(continues with,pinging wigle.net if wigle.net is up,
     #and continues uploading the logfile,deleting the uploaded file from /kismet-logs, disconnects from the wlan node and resumes (restarts kismet?)
    GPIO.output(9, True)#Turns off LED5
 
def connectivityTest():
    #Pings wigle.net
    thePing = subprocess.Popen('ping -c 5 wigle.net', shell=True, stdout=PIPE, stderr=PIPE)
    pingOut, pingErr = thePing.communicate()
    if len(pingErr) > 0: #If the ping fails ping 8.8.8.8
        thePing = subprocess.Popen('ping -c 5 8.8.8.8', shell=True, stdout=PIPE, stderr=PIPE)
        pingOut, pingErr = thePing.communicate()
        print 1
        if len(pingErr) > 0:#If pinging 8.8.8.8 fails display there is no internet connection
            print "There is no internet connectivity"
            return False
        else:#If pinging 8.8.8.8 succeeds, display there is no DHCP service.
            print "There is no DHCP server"
            return False
    else:
        print "There is connectivity"
        return True

