import picoESP8266 as esp8266
from machine import Pin
from time import sleep
import re, math

SSID = 'WiFimodem-7D90'
PWD = 'zwy3uznxkd'

esp = esp8266.Esp8266()
pump_01 = Pin(5, Pin.OUT)
pump_02 = Pin(4, Pin.OUT)
pump_03 = Pin(3, Pin.OUT)
pump_04 = Pin(2, Pin.OUT)
pump_01.value(1)
pump_02.value(1)
pump_03.value(1)
pump_04.value(1)

pumps = {'1':pump_01,
         '2':pump_02,
         '3':pump_03,
         '4':pump_04}

esp.blink()
esp.setMode('Station')
esp.WiFiConnect(SSID, PWD)
esp.server(80)

def read_html(filename):
    with open(filename, 'r') as f:
        html = ''
        for line in f.readlines():
            line = line.strip()
            html+=line
    return html

def send_index(esp):
    html = read_html('website.html')
    esp.client.send(html)

def send_page(esp, html_page):
    html = read_html(html_page)
    esp.client.send(html)

def pump_water(request):
    pump_nr = request[1].split('+')[1]
    ml = find_ml(request[1])
    t = flow(ml)
    html = read_html('wateringPlant.html')
    html = html.replace('{nr}', pump_nr)
    html = html.replace('{delay}', str(int(t)+5))
    html = html.replace('{ip}', esp.ip)
    esp.client.send(html)
    esp.client.close()
    pumps[pump_nr].value(0)
    sleep(t)
    pumps[pump_nr].value(1)
    
def find_ml(txt:str):
    ml_matcher = re.compile(r'ml=\d+')
    mtch = ml_matcher.search(txt)
    ml = mtch.group(0)
    return int(ml.split('=')[-1])

def tube_volume(length, diameter):
    #volume = r^2 * pi
    radius = diameter/2
    length = length*10 # from cm to mm
    return ((radius**2 * math.pi)*length)/1000

def flow(V, G=50):
    # time motor is on = volume[ml] * flowfactor [ms/ml] + tube [ms]
    # for some reason when i tested the tubes they all delivered 100 ml per 5 second
    # regardless of the tubes length. very confused
    # so for now the flow is as follows t[sec] = (V[ml] * flowfactor[ms/ml])/1000
    return (V * G)/1000

tube_length = 130 #cm
tube_diameter = 6.5 #mm
v = tube_volume(tube_length, tube_diameter)

while True:
    if esp.client:
        request = esp.client.GETrequest()
        if request[1] == '/':
            send_index(esp)
            esp.client.close()

        elif '/get?pump+' in request[1]:
            pump_water(request)

        
        elif 'GET /favicon.ico' in request[1]:
            send_index(esp)
            esp.client.close()
    pass
