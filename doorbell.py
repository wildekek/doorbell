"""
This script handles your RPi doorbel events:
- Prowl to send out a push notification
- Use HDMI to switch on TV to proper input
Todo:
- show live webcam feed on TV
- send webcam screenshot in push message
"""

import ConfigParser
import prowlpy
import RPIO
import time
import string
from subprocess import Popen, PIPE, STDOUT


global config
global prowl
global TvCecId

TvCecId = 0

# Read my config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

# Create a prowl object for push notifications
prowl = prowlpy.Prowl(config.get("prowl", "apikey"))


def gpio_callback(gpio_id, val):
    #print("gpio %s: %s" % (gpio_id, val))
    if ( gpio_id == config.getint("GPIO", "doorbellport") ) :
        if ( val == 1 ) :
            print ("Doorbell rang")
            send_notification()
            showRpiOnTV()

def send_notification():
    try:
        prowl.add('Doorbell','There is someone at the door!',"You could like open up for example", 1, None, config.get("webcam", "url"))
    except Exception,msg:
        print msg

def cec_command(deviceId, command):
    """
    Allows you to send CEC commands to a HDMI device using libCEC
    Examples: pow, standby, on, as
    For more info: https://github.com/Pulse-Eight/libcec

    FIXME: This function uses the cec-client command line tool, which is error-prone
    """

    # Use the command line tool    
    p = Popen(['cec-client', '-s', '-d', '1'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout = p.communicate(input = command + ' ' + str(deviceId))[0]

    # Format the stdout into something useful
    output = stdout.splitlines()
    try:
        output[1] = output[1].split(': ')
    except:
        pass

    # Do error handling

    # Return some usefull stuff
    return output


def showRpiOnTV():
	# Get the TV status
	powerStatus = cec_command(TvCecId, 'pow')[1][1]

	if powerStatus != 'on':
	        # Turn the tv on
	        cec_command(TvCecId, 'on')

	        # Wait for the TV to be ready
	        while True:
	                time.sleep(1)
	                powerStatus = cec_command(TvCecId, 'pow')[1][1]
	                if powerStatus == 'in transition from standby to on' or powerStatus == 'on':
	                    break

	# Set this device as TV input
	cec_command(TvCecId, 'as')



# GPIO interrupt callbacks
RPIO.add_interrupt_callback(config.getint("GPIO", "doorbellport") , gpio_callback, pull_up_down=RPIO.PUD_DOWN)

# Blocking main epoll loop
RPIO.wait_for_interrupts()
