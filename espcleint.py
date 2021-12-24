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

def turn_to_MAC(data):
    return ':'.join('%02x' % b for b in data)

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

  temp = str(esp32.raw_temperature())
  hall = str(esp32.hall_sensor())
  print("Temperature is " + temp)
  print("Hall is " + hall)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  address = socket.getaddrinfo('api.thingspeak.com', 80)[0][-1]
  s.connect(address)
  url="https://api.thingspeak.com/update?api_key=GHRXR4LGYL5FSWD1&field1="+temp+"&field2="+hall
  _, _, host, path = url.split('/', 3)
  print(host,path)
  #s.send(GET url+apikey+fields HTTP/1.0\r\nHost: api.thingspeak.com\r\n\r\n)
  a=s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
  print(a)
  #s.sendall("GET https://api.thingspeak.com/update?api_key=X99LDTAOIO14A5HW&field1="+temp+"&field2="+hall+"HTTP/1.0\r\nHost: api.thingspeak.com\r\n\r\n")
  #s.send("GET https://api.thingspeak.com/update?api_key=SBWKGQYKS3FC2Z5L&field1="+temp+"&field2="+hall+ HTTP/1.0\r\nHost: api.thingspeak.com\r\n\r\n)
  #(s.recv(1024))
  counter += 1
  s.close()
  
if __name__ == "__main__": 
    connect_wifi()
    counter = 0
    hardTimer = Timer(1)
    hardTimer.init(mode=Timer.PERIODIC, period=16000, callback=lambda t:Send(counter))
    print("Server Communicated")
