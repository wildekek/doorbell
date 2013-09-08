"""
This script triggers Prowl to send out a push notification
"""
import ConfigParser
import prowlpy
import RPIO

global config
global prowl

# Read my config file
config = ConfigParser.ConfigParser()
config.read('doorbell.ini')

# Create a prowl object for push notifications
prowl = prowlpy.Prowl(config.get("prowl", "apikey"))


def gpio_callback(gpio_id, val):
    #print("gpio %s: %s" % (gpio_id, val))
    if ( gpio_id == config.getint("GPIO", "doorbellport") ) :
        if ( val == 1 ) :
            print ("Doorbell rang")
            send_notification()

def send_notification():
    try:
        prowl.add('Doorbell','There is someone at the door!',"You could like open up for example", 1, None, 'http://192.168.192.5/gpio_status')
        print 'Push message sent!'
    except Exception,msg:
        print msg

# GPIO interrupt callbacks
RPIO.add_interrupt_callback(config.getint("GPIO", "doorbellport") , gpio_callback, pull_up_down=RPIO.PUD_DOWN)

# Blocking main epoll loop
RPIO.wait_for_interrupts()
