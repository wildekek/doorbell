"""
This script triggers Prowl to send out a push notification
"""
import prowlpy

apikey = '305209cbe316bdc8112635a11895a45c4ae1d70d'
p = prowlpy.Prowl(apikey)
try:
    p.add('Doorbell','There is someone at the door!',"You could like open up for example", 1, None, 'http://192.168.192.5/gpio_status')
    print 'Success'
except Exception,msg:
    print msg
