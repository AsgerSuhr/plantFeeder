import socket, ap_server, plant_server, network, tinyweb, os, time
from machine import Pin
from utime import sleep

# Define SSID and password for the access point
ap_ssid = "plantfeeder"
ap_password = "123456789"

# check if wifi credentials are store
if 'secrets.txt' in os.listdir():
    # read the file
    with open('secrets.txt', 'r') as f:
        lines = f.readlines()
    ssid, password = ' '.join(lines[0].split()), ' '.join(lines[1].split())
    net = network.WLAN(network.STA_IF)
    net.active(True)
    net.connect(ssid, password)
    
    # try and connect
    max_wait = 10
    while max_wait > 0:
        if net.status() < 0 or net.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
        
    if net.status() != 3:
        # start the AP server so that the user can connect the device to wifi
        print('network connection failed')
        ap_server.run(ap_ssid, ap_password)
    else:
        print('connected')
        status = net.ifconfig()
        print( 'ip = ' + status[0] )
        
        # start the plant watering website
        plant_server.run(net)
        
else:
    #start the AP server so that the user can connect the device to wifi
    ap_server.run(ap_ssid, ap_password)
        
