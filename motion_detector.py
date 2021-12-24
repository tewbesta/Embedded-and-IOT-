import machine
from network import *
from urequests import *
from time import *
from machine import I2C
sda = machine.Pin(23)
scl = machine.Pin(22)
i2c = machine.I2C(scl=scl, sda=sda,freq=400000)
devices = i2c.readfrom_mem(0x53, 0x00, 1)
print(devices)
for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
    if (device) != 229:
      print("No i2c device !")
    else:
      print('i2c devices found')
def convert(val):
    if val & (1 << 15):
        val = val - 1 << 16
    return val

from machine import Pin
from machine import Timer
from machine import RTC
from ntptime import time
import machine
import dht
import esp32
import usocket
import socket
import ssl
import network
import ubinascii,urequests,time
green=Pin(25,Pin.OUT)
red=Pin(26,Pin.OUT)

def connect_wifi():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('AndroidAP4505','12345678')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
def Send(counter):
      cloud="https://api.thingspeak.com/channels/1605243/feeds.json?api_key=5MMSPP9OR9BLOJ4E&results=2"
      k=get(cloud).text
      print("activate",'99' in k)
      if ('99' in k):
          i2c.writeto_mem(83, 0x2D, b"\x08")
          ax = convert(int.from_bytes(i2c.readfrom_mem(83, 0x33, 1) + i2c.readfrom_mem(83, 0x32, 1), "big"))/25
          ay = convert(int.from_bytes(i2c.readfrom_mem(83, 0x35, 1) + i2c.readfrom_mem(83, 0x34, 1), "big"))/25
          az = convert(int.from_bytes(i2c.readfrom_mem(83, 0x37, 1) + i2c.readfrom_mem(83, 0x36, 1), "big"))/(25)
          print("Acceleration on XYZ =", ax, ay, az)
          axs = str(ax)
          ays = str(ay)
          azs = str(az)
          
          print("ax is " + axs)
          print("ay is " + ays)
          
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          address = socket.getaddrinfo('api.thingspeak.com', 80)[0][-1]
          s.connect(address)
          url="https://api.thingspeak.com/update?api_key=GHRXR4LGYL5FSWD1&field1="+axs+"&field2="+ays+"&field3="+azs
          
          _, _, host, path = url.split('/', 3)
          print(host,path)
          a=s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
          print(host,path)
          print(a)
          green.off
          red.off
          if (abs(ax) <= 0.4 or abs(ay) <= 0.6 or abs(az) <= 10):
            green.on()
            red.off()
          else:
            green.off()
          if (abs(ax) > 0.4 or abs(ay) > 0.6 or abs(az) > 10):
              green.off()
              red.on()
              ifttt_data = {'value1': axs,'value2': ays,'value3': azs}
              request_headers = {'Content-Type': 'application/json'}

              response=urequests.post("https://maker.ifttt.com/trigger/motion/with/key/gmxOJludrdzwg4dEma5WZ2IZ6JI_TFZ-pADS--PzWix", json=ifttt_data, headers=request_headers)
              response.close()
              counter += 1
              s.close()
              return
          else:
            red.off()
  
if __name__ == "__main__": 
    connect_wifi()
    green.off
    red.off
    counter = 0
    hardTimer = Timer(1)
    hardTimer.init(mode=Timer.PERIODIC, period=16000, callback=lambda t:Send(counter))
    print("Server Communicated")


