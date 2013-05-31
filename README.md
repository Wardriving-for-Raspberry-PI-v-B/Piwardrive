Piwardrive
==========

A Wardriving script for Rasberry Pi v. B.
Functions:
A Led marked GPSD that lights if GPSD is running ok.
A Led that signals if kismet is running.
A led that shows if the GPS has a position fix.
A LED marked POEWER that goes dark if Raspberry has done a safe halt, and power can be disconnected without 
risking damage to the system.
A LED that lights up when upload to wigle.net is in progress.
This will only happen if: Your home wlan node is in reach, the Raspberry is connected to it, and wigle.net is reachable.
A momentarly closed switch triggers the action, it is marked Upload on the pcb.

The ON/OFF momentarly closed switch 
applies  power to the USB header, 
and keep it ON while the Raspberry Pi initializes and starts its application programs.
It works as described:
When input power is first applied, the MOSFET power switch comes up in its OFF state if the jumper is in the 
Auto-OFF position, or ON in the Auto-ON position. 
When your Raspberry Pi is ON, a momentary button press doesn't affect the power switch, but it is detected by the Raspberry. 
It is configured to produce an interrupt on a falling edge, or if polled frequently enough. 
This causes the command "shutdown -h -p now" to be activated, and
your RPi can then implement an orderly shut-down. 
When the Rasberry has shut down, the POWER LED will go dark.
You can then safely remove power.

The pinout is:
(POWER)pin1=3.3Vdc	pin6=GND
(kismet)pin7=GPIO4	pin12=GPIO18(upload)
(GPSD)	pin11=GPIO17	pin18=GPIO24(GPSLOCK)
(upload)pin15=GPIO22	pin22=GPIO25(powerSW)
pin25=GND
So far, the GPSD "OK" LED bit is tested and working, more to come...


Licence: Creative Commons Attribution-NonCommercial 3.0 Unported.

