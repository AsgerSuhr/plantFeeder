import picoESP8266 as esp8266
from machine import Pin
from time import sleep
import re

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

esp.blink()
esp.setMode('Station')
esp.WiFiConnect(SSID, PWD)


@esp.route('/')
def home():
    return "Hello! this is the main page <h1>HELLO</h1>"

esp.server(80)
'''
def flow(ML, G, K):
    # time motor is on = V[ml] * flowfactor [ms/ml] + tube [ms]
    return (ML * G + K)/1000

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
    print('so?s')
    esp.client.send(html)

def find_ml(txt:str):
    ml_matcher = re.compile(r'ml=\d+')
    mtch = ml_matcher.search(txt)
    ml = mtch.group(0)
    return int(ml.split('=')[-1])
    

while True:
    if esp.client:
        request = esp.client.GETrequest()
        if request[1] == '/':
            send_index(esp)
            esp.client.close()

        elif '/get?pump+1' in request[1]:
            send_page(esp, 'wateringPlant.html')
            esp.client.close()
            ml = find_ml(request[1])
            t = flow(ml, 57, 350)
            pump_01.value(0)
            sleep(t)
            pump_01.value(1)

        elif '/get?pump+2' in request[1]:
            send_page(esp, 'wateringPlant.html')
            esp.client.close()
            ml = find_ml(request[1])
            t = flow(ml, 57, 350)
            pump_02.value(0)
            sleep(t)
            pump_02.value(1)

        elif '/get?pump+3' in request[1]:
            send_page(esp, 'wateringPlant.html')
            esp.client.close()
            ml = find_ml(request[1])
            t = flow(ml, 57, 350)
            pump_03.value(0)
            sleep(t)
            pump_03.value(1)
            
        elif '/get?pump+4' in request[1]:
            send_page(esp, 'wateringPlant.html')
            esp.client.close()
            ml = find_ml(request[1])
            t = flow(ml, 57, 350)
            pump_04.value(0)
            sleep(t)
            pump_04.value(1)
        
        elif 'GET /favicon.ico' in request[1]:
            send_index(esp)
            esp.client.close()
    pass

'''