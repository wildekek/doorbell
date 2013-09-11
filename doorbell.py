"""
This script triggers Prowl to send out a push notification
when a doorbell is pressed on the RPI GPIO
"""
import ConfigParser
import prowlpy
import RPIO

global config
global prowl

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
            switch_tv()

def send_notification():
    try:
        prowl.add('Doorbell','There is someone at the door!',"You could like open up for example", 1, None, config.get("webcam", "url"))
        print 'Push message sent!'
    except Exception,msg:
        print msg

def switch_tv():
    exec(echo "pow 0" | cec-client -s -d 1)

# GPIO interrupt callbacks
RPIO.add_interrupt_callback(config.getint("GPIO", "doorbellport") , gpio_callback, pull_up_down=RPIO.PUD_DOWN)

# Blocking main epoll loop
RPIO.wait_for_interrupts()
