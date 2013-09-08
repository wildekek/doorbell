"""
This script triggers Prowl to send out a push notification
"""
import ConfigParser
import prowlpy

config = ConfigParser.ConfigParser()
config.read('doorbell.ini')

apikey = config.get("prowl", "apikey")
print apikey

p = prowlpy.Prowl(apikey)
try:
    p.add('Doorbell','There is someone at the door!',"You could like open up for example", 1, None, 'http://192.168.192.5/gpio_status')
    print 'Success'
except Exception,msg:
    print msg
