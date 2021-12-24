import machine,esp32
import network
from machine import TouchPad, Pin, RTC,Timer
import ntptime
import utime
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Lark')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    print("Connected to AndroidAP4505 12345678")
do_connect()
#ntptime.settime()
rtc = machine.RTC()
utc_shift = 3
tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
tm = tm[0:3] + (0,) + tm[3:6] + (0,)
rtc.datetime(tm)
myDateTimeTimer = Timer(0)
myDateTimeTimer.init(mode=Timer.PERIODIC, period=15000, callback=lambda x:print("Date: ", rtc.datetime()[2], "/", rtc.datetime()[1], "/", rtc.datetime()[0], "\n Time: ", rtc.datetime()[4]+5, ":", rtc.datetime()[5], ":", rtc.datetime()[6]))
t = TouchPad(Pin(14))
timer1=Timer(1)
timer2=Timer(2)
green=Pin(25,Pin.OUT)
red=Pin(26,Pin.OUT)
green.value(0)
def touch(p):

    if(t.read()>600):
      print("touch")
      green.value(1)
    else:
      green.value(0)
      print("not touched")
    print("touch function")
def sleepy(p):
 #sleep(0.05)


     print("I am going to sleep for 1 minute")
     red.value(0)
     machine.lightsleep(60000)
     print("Woke due to timer")
     red.value(1)
switch = Pin(39,Pin.IN)
if switch.value()==0:
    red.value(1)
    esp32.wake_on_ext1([switch], esp32.WAKEUP_ANY_HIGH)
    esp32.wake_on_touch(True)
    print("Woke up due to EXT0 wakeup.")
    
timer1.init(mode=Timer.PERIODIC, period=50000, callback=touch)
timer2.init(mode=Timer.PERIODIC, period=30000, callback=sleepy)
