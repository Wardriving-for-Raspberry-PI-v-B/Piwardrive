import RPi.GPIO as GPIO
import os
import subprocess
import gps
import time
from ConfigParser import SafeConfigParser
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(04, GPIO.OUT)#LED1 KISMET
GPIO.setup(17, GPIO.OUT)#LED2 GPSD running
GPIO.setup(9, GPIO.OUT)#LED5 Upload in progress.
GPIO.setup(26, GPIO.IN)#Data upload switch,momentarily toggle.
GPIO.setup(7 , GPIO.IN)#Power off button.
GPIO.output(04, True)#Makes sure all LED's are at the same state initially (off):
GPIO.output(17, True)
GPIO.output(22, True)
GPIO.output(9, True)
GPIO.output(10, True)

configFile = SafeConfigParser()#Sets up a parser for the Config File
configFile.read('wardrive.config')#Reads the wardrive.config file.

##The following while loop is the main code execution
while True:
    executeKismet()
    executeGPS()
    while True:
        if (GPIO.input(26)): #If upload button is pressed
            uploadButton()
        if (GPIO.input(7)): #If power button is pressed
            os.system("shutdown -h now")


def executeKismet():
    kismet = subprocess.Popen(['ps -ef | grep kismet'],
    stdout=subprocess.PIPE, shell=True) #Assigns the output from the grep to the kismet variable
    (output, error) = kismet.communicate()
    if 'kismet_server' in output:
        GPIO.output(04, False) #Turn on KISMET LED
    else:
        GPIO.output(04, True) #Turn off KISMET LED
        
def executeGPS():
    gps = subprocess.Popen(['ps -ef | grep gpsd'],
    stdout=subprocess.PIPE, shell=True)#Assigns the output from the grepto the gps variable
    (output, error) = gps.communicate()
    if 'gpsd' in output:
        GPIO.output(17, False) #Turn on GPSD LED
    else:
        GPIO.output(17, True) #Turn off GPSD LED
        
def uploadButton():
    time.sleep(0.05)
    os.system("killall kismet")
    time.sleep(3)# added so kismet has the time to die.
    os.system("iwconfig wlan0 essid " + configFile.get('Home Wireless Setup', 'ssid') + " key " + configFile.get('Home Wireless Setup', 'network_key'))#Connects to your home Wireless
    time.sleep(10)# added so wlan0 has time to autenticate and assosiate with the wlan node
    if connectivityTest(): #Checks for internet connectivity. (Mainly connectivity to wigle.net)
        print "This executes when there is connectivity to wigle.net"
        GPIO.output(9, False)#Turns on upload LED
        wigleUsername = configFile.get('Wigle.net Setup', 'wigleUsername')
        wiglePassword = configFile.get('Wigle.net Setup', 'wiglePassword')
        #This grabs the authentication cookie used when uploading a file (its login into wigle.net). The cookie is stored in the current directory in a file called wigleCookie.txt
        loginAndCookieGrab = subprocess.Popen("curl -c wigleCookie.txt -d \"credential_0=" + wigleUsername + "&credential_1=" + wiglePassword +" https://wigle.net/gps/gps/main/login/", shell=True, stdout=PIPE, stderr=PIPE)
        loginAndCookieGrabOut, loginAndCookieGrabErr = loginAndCookieGrab.communicate()
        #This uploads the output file from kismet to wigle.net. It used the cookie retrived from before during the upload process so it is authenticated.
        upload = subprocess.Popen("curl -b wigleCookie.txt -F \"stumblefile=@/var/log/kismet -d \"Send=Send&observer=" + wigleUsername + " https://wigle.net/gps/gps/main/postfile", shell=True, stdout=PIPE, stderr=PIPE)
        uploadOut, uploadErr = upload.communicate()
        #Then deleting the uploaded file from /kismet-logs, disconnects from the wlan node and resumes (restarts kismet?)
    else:
        print "This executes when there is no connectivity to wigle.net"#Line to be removed (Used for Dubugging)
    GPIO.output(9, True)#Turns off upload LED
    
    
def connectivityTest():
    #Pings wigle.net
    thePing = subprocess.Popen('ping -c 5 wigle.net', shell=True, stdout=PIPE, stderr=PIPE)
    pingOut, pingErr = thePing.communicate()
    if len(pingErr) > 0: #If the ping fails ping 8.8.8.8
        thePing = subprocess.Popen('ping -c 5 8.8.8.8', shell=True, stdout=PIPE, stderr=PIPE)
        pingOut, pingErr = thePing.communicate()
        print 1
        if len(pingErr) > 0:#If pinging 8.8.8.8 fails display there is no internet connection
            print "There is no internet connectivity"#Line to be removed (Used for Dubugging)
            return False
        else:#If pinging 8.8.8.8 succeeds, display there is no DHCP service.
            print "There is no DHCP server"#Line to be removed (Used for Dubugging)
            return False
    else:
        print "There is connectivity"#Line to be removed (Used for Dubugging)
        return True
