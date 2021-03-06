#!/usr/bin/env python 
#This is a startup script that starts the processes needed for Piwardrive.
#It needs to be executed atomatic on boot. Edit your crontab file with the command crontab -e, add @reboot python  /home/pi/Piwardrive/startup.py.
#press ctrl + o to save the file. if everything is ok, crontab spits out crontab: installing new crontab when the file is saved.
#This file needs to be set as a executable file with: chmod 755 /home/pi/Piwardrive/startup.py
#
#
import os
import time
os.system("gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock")#starts up gpsd using the default USB port.
time.sleep(2.5)#Added in case gpsd needs some time to start up
os.system("kismet_server -s --daemonize")#starts up kismet_server in the background.
os.system("python /home/pi/Piwardrive/gpsfix.py")#starts up the script that controlls the GPSLOCK LED.
os.system("python /home/pi/Piwardrive/wardrive.py")#starts up the main script.
#NOTES:
#kismet_server reads config file /usr/local/etc/kismet.conf upon start,
#so that needs to be set up as kismet_server will NOT run properly without! PLEASE DISABLE THE PLUGINS!
#The complete list of 2.5 ghz and 5ghz wlan channels is here: https://en.wikipedia.org/wiki/List_of_WLAN_channels
#5 ghz (802.11a) is not wery common in use, but should be included in the channel list along with the normal 
#2.5ghz (802.11b/g) channels.
