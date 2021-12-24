# Global variables
import esp32
import socket
from machine import Pin
temp = str(esp32.raw_temperature())
hall = str(esp32.hall_sensor()) # measure temperature sensor data
    # measure hall sensor data
red_led_state="OFF" # string, check state of red led, ON or OFF
green_led_state="OFF" # string, check state of red led, ON or OFF
switch_state="ON"

def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state, green_led_state
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
     Switch Current State: <strong>""" + switch_state + """</strong>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p>
    <a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('AndroidAP4505', '12345678')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
do_connect()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
green_led = Pin(26, Pin.OUT)
red_led = Pin(25, Pin.OUT)
switch = Pin(34,Pin.IN,Pin.PULL_UP)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  green_led_on = request.find('/?green_led=on')
  green_led_off = request.find('/?green_led=off')
  red_led_on = request.find('/?red_led=on')
  red_led_off = request.find('/?red_led=off')
  if switch.value()==0:
       print('switch OFF')
       switch_state="OFF"
  else:
      print("switch ON")
      switch_state="ON"
  if green_led_on == 6:
    print('green_led ON')
    green_led.value(1)
    green_led_state="ON"
  if green_led_off == 6:
    print('green_led OFF')
    green_led.value(0)
    green_led_state="OFF"
  if red_led_on == 6:
    print('red_led ON')
    red_led.value(1)
    red_led_state="ON"
  if red_led_off == 6:
    print('red_led OFF')
    red_led.value(0)
    red_led_state="OFF"
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()